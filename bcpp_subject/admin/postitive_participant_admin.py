from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..forms import PositiveParticipantForm
from ..models import PositiveParticipant

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PositiveParticipant, site=bcpp_subject_admin)
class PositiveParticipantAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PositiveParticipantForm
    fields = (
        "subject_visit",
        'internalize_stigma',
        'internalized_stigma',
        'friend_stigma',
        'family_stigma',
        'enacted_talk_stigma',
        'enacted_respect_stigma',
        'enacted_jobs_tigma',)
    radio_fields = {
        "internalize_stigma": admin.VERTICAL,
        "internalized_stigma": admin.VERTICAL,
        "friend_stigma": admin.VERTICAL,
        "family_stigma": admin.VERTICAL,
        "enacted_talk_stigma": admin.VERTICAL,
        "enacted_respect_stigma": admin.VERTICAL,
        "enacted_jobs_tigma": admin.VERTICAL, }
    instructions = [(
        "<h5>Interviewer Note</h5> The following supplemental questions"
        " are only asked for respondents with known HIV infection."
        " SKIP for respondents without known HIV infection. "),
        _(" Read to Participant: You let us know earlier that you"
          " are HIV positive. I would now like to ask you a few"
          " questions about your experiences living with HIV."
          " Please remember this interview and your responses"
          " are private and confidential.In this section,"
          " I'm going to read you statements"
          "  about how you may feel about yourself and your "
          " HIV/AIDS infection. I would like you to tell me"
          " if you strongly agree, agree, disagree or strongly"
          " disagree with each statement?")]
