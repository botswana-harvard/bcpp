from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..constants import BASELINE, ANNUAL
from ..models import MedicalDiagnoses
from ..forms import MedicalDiagnosesForm

from .modeladmin_mixins import CrfModelAdminMixin, SubjectAdminExcludeMixin


@admin.register(MedicalDiagnoses, site=bcpp_subject_admin)
class MedicalDiagnosesAdmin(SubjectAdminExcludeMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalDiagnosesForm
    fields = (
        'subject_visit',
        'diagnoses',
        'heart_attack_record',
        'cancer_record',
        'tb_record',
    )
    radio_fields = {
        "heart_attack_record": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "tb_record": admin.VERTICAL, }
    filter_horizontal = ('diagnoses',)
    instructions = {
        BASELINE: [_(
            "<h5>Read to Participant</h5> I am now going to ask you"
            " some questions about major illnesses that you may"
            " have had in the past 12 months. Sometimes people"
            " call different sicknesses by different names."
            " If you do not understand what I mean, please ask."
            " Also, please remember that your answers will be"
            " kept confidential. (baseline)")],
        ANNUAL: [_(
            "<h5>Read to Participant</h5> I am now going to ask you"
            " some questions about major illnesses that you may"
            " have had since we spoke with you at our last visit. Sometimes people"
            " call different sicknesses by different names."
            " If you do not understand what I mean, please ask."
            " Also, please remember that your answers will be"
            " kept confidential. (annual)")]
    }
