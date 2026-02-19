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

from __future__ import annotations

import logging

from typing import List, Set

from ....const import GRAMPS_LOCALE as glocale
from ....db import Database
from ....lib import Person
from .. import Rule

_ = glocale.translation.gettext
LOG = logging.getLogger(".filters.person.relatedwithhome")


def _collect_related_handles(db: Database, start: Person | None) -> Set[str]:
    """
    Return all people in the same family-relationship graph component as start.
    """
    selected_handles: Set[str] = set()
    if not start:
        return selected_handles

    queue: List[Person] = [start]
    while queue:
        person = queue.pop()
        if person is None or (person.handle in selected_handles):
            continue

        selected_handles.add(person.handle)

        for family_handle in person.parent_family_list:
            family = db.get_family_from_handle(family_handle)
            if not family:
                continue
            for parent_handle in (family.father_handle, family.mother_handle):
                if parent_handle:
                    queue.append(db.get_person_from_handle(parent_handle))
            for child_ref in family.child_ref_list:
                queue.append(db.get_person_from_handle(child_ref.ref))

        for family_handle in person.family_list:
            family = db.get_family_from_handle(family_handle)
            if not family:
                continue
            for parent_handle in (family.father_handle, family.mother_handle):
                if parent_handle:
                    queue.append(db.get_person_from_handle(parent_handle))
            for child_ref in family.child_ref_list:
                queue.append(db.get_person_from_handle(child_ref.ref))

    return selected_handles


class _RelatedWithPersonOrHomeBase(Rule):
    """
    Shared anchor resolution and traversal for related/not-related filters.
    """

    labels = [
        _("Anchor mode (home_person|explicit_person_id):"),
        _("Person ID (required for explicit mode):"),
    ]
    category = _("Relationship filters")

    def prepare(self, db: Database, user):
        self.related_handles: Set[str] = set()
        self.anchor_valid = False

        raw_mode = self.list[0].strip().lower() if len(self.list) > 0 else ""
        person_id = self.list[1].strip() if len(self.list) > 1 else ""

        # Backward-compatible shorthand: one non-empty parameter means person ID.
        if len(self.list) == 1 and raw_mode not in (
            "",
            "home_person",
            "home",
            "default_person",
            "default",
            "explicit_person_id",
            "explicit",
            "person_id",
            "id",
        ):
            person_id = self.list[0].strip()
            mode = "explicit_person_id"
        elif raw_mode in ("", "home_person", "home", "default_person", "default"):
            mode = "home_person"
        elif raw_mode in ("explicit_person_id", "explicit", "person_id", "id"):
            mode = "explicit_person_id"
        else:
            mode = "home_person"

        anchor_person: Person | None = None
        if mode == "explicit_person_id":
            if person_id:
                anchor_person = db.get_person_from_gramps_id(person_id)
            if anchor_person is None:
                LOG.warning(
                    "Relationship filter anchor unresolved for explicit ID '%s'",
                    person_id,
                )
                return
        else:
            anchor_person = db.get_default_person()
            if anchor_person is None:
                LOG.warning(
                    "Relationship filter requested Home Person anchor, but no Home Person is set"
                )
                return

        self.anchor_valid = True
        self.related_handles = _collect_related_handles(db, anchor_person)

    def reset(self):
        self.related_handles.clear()
        self.anchor_valid = False


class IsRelatedWithPersonOrHome(_RelatedWithPersonOrHomeBase):
    """
    Rule that checks if a person is related to an explicit person or Home Person.
    """

    name = _("People related to <Person/Home Person>")
    description = _(
        "Matches people related via family links to an explicit person or Home Person"
    )

    def apply_to_one(self, db: Database, person: Person) -> bool:
        if not self.anchor_valid:
            return False
        return person.handle in self.related_handles

    def prepare(self, db: Database, user):
        super().prepare(db, user)
        # Expose selected_handles for optimizer shortcut only on related rule.
        self.selected_handles = self.related_handles

    def reset(self):
        super().reset()
        self.selected_handles = set()


class IsNotRelatedWithPersonOrHome(_RelatedWithPersonOrHomeBase):
    """
    Rule that checks if a person is not related to an explicit person/Home Person.
    """

    name = _("People NOT related to <Person/Home Person>")
    description = _(
        "Matches people not related via family links to an explicit person or "
        "Home Person"
    )

    def apply_to_one(self, db: Database, person: Person) -> bool:
        if not self.anchor_valid:
            return False
        return person.handle not in self.related_handles
