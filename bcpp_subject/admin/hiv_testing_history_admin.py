from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..models import HivTestingHistory
from ..forms import HivTestingHistoryForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivTestingHistory, site=bcpp_subject_admin)
class HivTestingHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestingHistoryForm

    fields = (
        "subject_visit",
        'has_tested',
        "when_hiv_test",
        'has_record',
        'verbal_hiv_result',
        'other_record',)

    radio_fields = {
        "has_tested": admin.VERTICAL,
        "when_hiv_test": admin.VERTICAL,
        "has_record": admin.VERTICAL,
        "verbal_hiv_result": admin.VERTICAL,
        'other_record': admin.VERTICAL}

    instructions = [(
        "Do not include documentation of ART/PMTCT/CD4 here; "
        "only include actual HIV test results"),
        _("<H5>Read to Participant</H5> Many people have had a test"
          " to see if they have HIV. I am going to ask you"
          " about whether you have been tested for HIV and"
          " whether you received the results. Please"
          " remember that all of your answers are"
          " confidential.")]

    annual_verbose_name = {
        "has_tested": (
            "Since we last visited you have you been tested for HIV? "
            "If yes, go on with form, if not, SKIP"),
        "when_hiv_test": (
            "If yes,  you have tested since we last visited you, "
            "when was this test you had since we last visited you?"),
    }
