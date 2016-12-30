from django.test import TestCase

from member.tests.test_mixins import MemberMixin
from ..views import EnumerationDashboardView
import arrow
from household.models.household_log_entry import HouseholdLogEntry


class TestEnumerationDashboard(MemberMixin, TestCase):

    def test_return_todays_household_log_entry(self):
        """Assert today's log entry is returned."""
        household_structure = self.make_household_ready_for_enumeration(make_hoh=False)
        enumeration_dashboard = EnumerationDashboardView()
        enumeration_dashboard.get_context_data(
            household_identifier=household_structure.household.household_identifier,
            survey=household_structure.survey)
        todays_household_log_entry = enumeration_dashboard.todays_household_log_entry(household_structure)
        r = arrow.Arrow.fromdatetime(todays_household_log_entry.report_datetime, todays_household_log_entry.report_datetime.tzinfo).to('utc')
        self.assertEqual(r.date(), arrow.utcnow().date())

    def test_no_todays_household_log_entry_returned(self):
        """Assert today's log entry is not returned if there are no household log entries or no today's log."""
        household_structure = self.make_household_ready_for_enumeration(make_hoh=False)
        HouseholdLogEntry.objects.all().delete()
        enumeration_dashboard = EnumerationDashboardView()
        todays_household_log_entry = enumeration_dashboard.todays_household_log_entry(household_structure)
        self.assertIsNone(todays_household_log_entry)
