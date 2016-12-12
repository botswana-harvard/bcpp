from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..forms import StigmaForm
from ..models import Stigma

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Stigma, site=bcpp_subject_admin)
class StigmaAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = StigmaForm
    fields = (
        "subject_visit",
        'anticipate_stigma',
        'enacted_shame_stigma',
        'saliva_stigma',
        'teacher_stigma',
        'children_stigma',)
    radio_fields = {
        "anticipate_stigma": admin.VERTICAL,
        "enacted_shame_stigma": admin.VERTICAL,
        "saliva_stigma": admin.VERTICAL,
        "teacher_stigma": admin.VERTICAL,
        "children_stigma": admin.VERTICAL, }
    instructions = [(
        "<h5>Interviewer Note</h5> The following supplemental "
        "questions are only asked for respondents NOT known"
        " to have HIV. SKIP for respondents with known HIV infection."
    ),
        _(" Read to Participant: Different people feel differently about"
          " people living with HIV. I am going to ask you about issues"
          " relevant to HIV and AIDS and also people living with HIV."
          " Some of the questions during the interview will ask for your"
          " opinion on how you think people living with HIV are treated."
          " To start, when thinking about yourself, please tell me how "
          " strongly you agree or disagree with the following statements.")]
