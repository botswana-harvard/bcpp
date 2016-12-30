import arrow

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from household.models.household import Household
from household.models.household_log import HouseholdLog
from household.models.household_log_entry import HouseholdLogEntry
from household.models.household_structure.household_structure import HouseholdStructure
from member.constants import HEAD_OF_HOUSEHOLD
from member.models import RepresentativeEligibility
from member.models.household_head_eligibility import HouseholdHeadEligibility
from member.models.household_member.household_member import HouseholdMember


class EnumerationDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'bcpp/enumeration_dashboard.html'
    paginate_by = 4

    def __init__(self, **kwargs):
        self.household_identifier = None
        self.survey = None
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.survey = context.get('survey')
        self.household_identifier = context.get('household_identifier')
        context.update(
            site_header=admin.site.site_header,
            household_log_entries=self.household_log_entries,
            household_members=self.household_members,
            household_log=self.household_log,
            household_structure=self.household_structure,
            representative_eligibility=self.representative_eligibility,
            head_of_household=self.head_of_household,
            head_of_household_eligibility=self.head_of_household_eligibility,
            todays_household_log_entry=self.todays_household_log_entry
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def household(self):
        """Return  a household."""
        try:
            obj = Household.objects.get(household_identifier=self.household_identifier)
        except Household.DoesNotExist:
            obj = None
        return obj

    @property
    def household_structure(self):
        """Return household structure."""
        try:
            obj = HouseholdStructure.objects.get(
                household__household_identifier=self.household_identifier, survey=self.survey)
        except HouseholdStructure.DoesNotExist:
            obj = None
        return obj

    @property
    def household_log(self):
        """Return household log."""
        try:
            obj = HouseholdLog.objects.get(household_structure=self.household_structure)
        except HouseholdLog.DoesNotExist:
            obj = None
        return obj

    @property
    def household_log_entries(self):
        """Return household log entries."""
        household_log_entries = HouseholdLogEntry.objects.filter(
            household_log__household_structure=self.household_structure).order_by('report_datetime')
        return household_log_entries

    @property
    def todays_household_log_entry(self):
        """Return today's household log entry."""
        try:
            obj = HouseholdLogEntry.objects.get(
                household_log__household_structure=self.household_structure,
                report_datetime__year=arrow.utcnow().year,
                report_datetime__month=arrow.utcnow().month,
                report_datetime__day=arrow.utcnow().day)
        except HouseholdLogEntry.DoesNotExist:
            obj = None
        return obj

    @property
    def household_members(self):
        """Return all household member for this household structure."""
        return HouseholdMember.objects.filter(
            household_structure=self.household_structure).order_by('report_datetime')

    @property
    def head_of_household(self):
        """Return the household member that is the Head of Household."""
        try:
            obj = HouseholdMember.objects.get(
                household_structure=self.household_structure,
                relation=HEAD_OF_HOUSEHOLD)
        except HouseholdMember.DoesNotExist:
            obj = None
        return obj

    @property
    def head_of_household_eligibility(self):
        """Return the head of household eligibility."""
        try:
            obj = HouseholdHeadEligibility.objects.get(
                household_member=self.head_of_household)
        except HouseholdHeadEligibility.DoesNotExist:
            obj = None
        return obj

    @property
    def representative_eligibility(self):
        """Return the representative eligibility."""
        try:
            obj = RepresentativeEligibility.objects.get(
                household_structure=self.household_structure)
        except RepresentativeEligibility.DoesNotExist:
            obj = None
        return obj
