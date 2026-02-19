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

from ....const import GRAMPS_LOCALE as glocale

_ = glocale.translation.gettext

from .. import Rule
from ._eventcitationutils import collect_person_and_linked_event_citation_handles

from ....db import Database
from ....lib import Person


class PersonMissingSourcesIncludingEvents(Rule):
    """
    People missing sources when person + linked events are considered together.
    """

    name = _("People missing sources (person + linked events)")
    category = _("Citation/source filters")
    description = _("Matches people with no sources in person records or linked events")

    def apply_to_one(self, db: Database, person: Person) -> bool:
        return len(collect_person_and_linked_event_citation_handles(db, person)) == 0
