#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2026
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.
#

"""
Helpers to collect person citations including linked event citations.
"""

from __future__ import annotations

from typing import Set

from ....db import Database
from ....lib import Person
from ....lib.eventref import EventRef


def collect_object_and_child_citation_handles(citation_obj) -> Set[str]:
    """
    Collect citation handles from an object and all citation-capable children.

    This avoids CitationBase.get_all_citation_lists() because that method
    mutates internal lists while aggregating.
    """
    citations: Set[str] = set()
    stack = [citation_obj]
    while stack:
        item = stack.pop()
        if item is None:
            continue
        if hasattr(item, "get_citation_list"):
            citations.update(
                citation for citation in item.get_citation_list() if citation
            )
        if hasattr(item, "get_citation_child_list"):
            stack.extend(item.get_citation_child_list())
    return citations


def _collect_event_ref_and_event_citations(
    db: Database, event_ref: EventRef | None, out: Set[str]
) -> None:
    """
    Add citations from an EventRef and its dereferenced Event object.
    """
    if event_ref is None:
        return

    out.update(collect_object_and_child_citation_handles(event_ref))

    if not event_ref.ref:
        return

    event = db.get_event_from_handle(event_ref.ref)
    if event is None:
        return

    out.update(collect_object_and_child_citation_handles(event))


def collect_person_and_linked_event_citation_handles(
    db: Database, person: Person
) -> Set[str]:
    """
    Return citation handles attached to:
    1. person direct/secondary citation locations
    2. linked EventRefs and their dereferenced Events
    3. linked Family EventRefs and their dereferenced Events
    """
    citations: Set[str] = collect_object_and_child_citation_handles(person)

    for event_ref in person.get_event_ref_list():
        _collect_event_ref_and_event_citations(db, event_ref, citations)

    for family_handle in person.get_family_handle_list():
        family = db.get_family_from_handle(family_handle)
        if family is None:
            continue
        for event_ref in family.get_event_ref_list():
            _collect_event_ref_and_event_citations(db, event_ref, citations)

    return citations
