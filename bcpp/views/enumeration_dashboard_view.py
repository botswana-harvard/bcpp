from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from member.models.household_member.household_member import HouseholdMember
from household.models.household import Household
from household.models.household_structure.household_structure import HouseholdStructure
from household.models.household_log_entry import HouseholdLogEntry
from household.models.household_log import HouseholdLog


class EnumerationDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'bcpp_dashboard/enumeration_dashboard.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data(**kwargs)
        self.context.update(
            site_header=admin.site.site_header,
            household_log_entries=self.household_log_entries(),
            household_members=self.household_members()
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

    def household_members(self):
        return HouseholdMember.objects.filter(household_structure=self.household_structure())

    def survey(self, survey=None):
        return self.context.get('survey')

    @property
    def household_identifier(self):
        return self.context.get('household_identifier')

    def household_structure(self):
        for h in HouseholdStructure.objects.all():
            print(h.survey)
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
