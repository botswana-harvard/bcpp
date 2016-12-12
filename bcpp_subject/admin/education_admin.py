from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL
from ..forms import EducationForm
from ..models import Education

from .modeladmin_mixins import CrfModelAdminMixin, SubjectAdminExcludeMixin


@admin.register(Education, site=bcpp_subject_admin)
class EducationAdmin(SubjectAdminExcludeMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = EducationForm

    fields = [
        "subject_visit",
        'education',
        'working',
        'job_type',
        'reason_unemployed',
        'job_description',
        'monthly_income']

    custom_exclude = {
        ANNUAL: [
            'education',
            'working',
            'job_type',
            'reason_unemployed']
    }

    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }

    instructions = [_("<H5>Read to Participant</H5> Next, I will ask you some "
                      "questions about what education and work you "
                      "may have done or are currently doing.")]
