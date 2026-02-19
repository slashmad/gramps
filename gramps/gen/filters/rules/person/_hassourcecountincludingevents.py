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

from .._hassourcecountbase import HasSourceCountBase
from ._eventcitationutils import collect_person_and_linked_event_citation_handles

from ....db import Database
from ....lib import Person


class PersonHasSourceCountIncludingEvents(HasSourceCountBase):
    """
    People with source count, including linked event citations.
    """

    name = _("People with <count> sources (person + linked events)")
    description = _(
        "Matches people with a certain number of sources connected to person "
        "records and linked events"
    )

    def apply_to_one(self, db: Database, person: Person) -> bool:
        count = len(collect_person_and_linked_event_citation_handles(db, person))
        if self.count_type == 0:  # "less than"
            return count < self.userSelectedCount
        elif self.count_type == 2:  # "greater than"
            return count > self.userSelectedCount
        # "equal to"
        return count == self.userSelectedCount
