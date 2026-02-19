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

from .._hassourceofbase import HasSourceOfBase
from ._eventcitationutils import collect_person_and_linked_event_citation_handles

from ....db import Database
from ....lib import Person


class PersonHasSourceOfIncludingEvents(HasSourceOfBase):
    """
    People with a specific source, including linked event citations.
    """

    labels = [_("Source ID:")]
    name = _("People with the <source> (person + linked events)")
    category = _("Citation/source filters")
    description = _(
        "Matches people who have a particular source in person or event data"
    )

    def apply_to_one(self, db: Database, person: Person) -> bool:
        citation_handles = collect_person_and_linked_event_citation_handles(db, person)

        if not self.source_handle:
            return self.nosource and len(citation_handles) == 0

        for citation_handle in citation_handles:
            citation = db.get_citation_from_handle(citation_handle)
            if citation and citation.source_handle == self.source_handle:
                return True

        return False
