from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from member.models.household_member.household_member import HouseholdMember
from member.models import RepresentativeEligibility
from household.models.household import Household
from household.models.household_structure.household_structure import HouseholdStructure
from household.models.household_log_entry import HouseholdLogEntry
from household.models.household_log import HouseholdLog
from member.models.household_head_eligibility import HouseholdHeadEligibility
from member.constants import HEAD_OF_HOUSEHOLD
import arrow


class EnumerationDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'enumeration_dashboard.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            site_header=admin.site.site_header,
            household_log_entries=self.household_log_entries(),
            household_members=self.household_members(),
            household_log=self.household_log,
            household_identifier=self.household_identifier,
            household_structure=self.household_structure(),
            representative_eligibility=self.representative_eligibility,
            head_of_household=self.head_of_household,
            head_of_household_eligibility=self.head_of_household_eligibility,
            todays_household_log_entry=self.todays_household_log_entry(self.household_structure())
        )
        return self.context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnumerationDashboardView, self).dispatch(*args, **kwargs)

    @property
    def household_log(self):
        try:
            household_log = HouseholdLog.objects.get(household_structure=self.household_structure())
        except HouseholdLog.DoesNotExist:
            household_log = None
        return household_log

    def household_log_entries(self):
        household_log_entries = HouseholdLogEntry.objects.filter(household_log=self.household_log)
        return household_log_entries

    def todays_household_log_entry(self, household_structure):
        todays_household_log_entry = None
        report_datetime = HouseholdLogEntry.objects.filter(
            household_log__household_structure=household_structure).aggregate(
                Max('report_datetime')).get('report_datetime__max')
        if report_datetime:
            r = arrow.Arrow.fromdatetime(report_datetime, report_datetime.tzinfo).to('utc')
            if r.date() == arrow.utcnow().date():
                todays_household_log_entry = HouseholdLogEntry.objects.get(
                    household_log__household_structure=household_structure,
                    report_datetime=report_datetime)
        return todays_household_log_entry

    def household_members(self):
        return HouseholdMember.objects.filter(household_structure=self.household_structure())

    @property
    def head_of_household(self):
        members = HouseholdMember.objects.filter(household_structure=self.household_structure())
        head_of_household = None
        for member in members:
            if member.relation == HEAD_OF_HOUSEHOLD:
                head_of_household = member
        return head_of_household

    @property
    def head_of_household_eligibility(self):
        try:
            head_of_household_eligibility = HouseholdHeadEligibility.objects.get(household_member=self.head_of_household)
        except HouseholdHeadEligibility.DoesNotExist:
            head_of_household_eligibility = None
        return head_of_household_eligibility

    @property
    def representative_eligibility(self):
        try:
            representative_eligibility = RepresentativeEligibility.objects.get(household_structure=self.household_structure())
        except RepresentativeEligibility.DoesNotExist:
            representative_eligibility = None
        return representative_eligibility

    def survey(self, survey=None):
        return self.context.get('survey')

    @property
    def household_identifier(self):
        return self.context.get('household_identifier')

    def household_structure(self):
        # survey bcpp-survey.bcpp-year-1.bhs.test_community
        try:
            household_structure = HouseholdStructure.objects.get(household=self.household, survey='bcpp-survey.bcpp-year-1.bhs.test_community')
        except HouseholdStructure.DoesNotExist:
            household_structure = None
        return household_structure

    @property
    def household(self):
        """Returns a household."""
        try:
            household = Household.objects.get(household_identifier=self.household_identifier)
        except Household.DoesNotExist:
            household = None
        return household
