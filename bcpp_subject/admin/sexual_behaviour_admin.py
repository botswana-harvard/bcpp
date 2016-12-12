from django.contrib import admin
from django.utils.translation import ugettext as _

from ..admin_site import bcpp_subject_admin
from ..forms import SexualBehaviourForm
from ..models import SexualBehaviour

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SexualBehaviour, site=bcpp_subject_admin)
class SexualBehaviourAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SexualBehaviourForm
    fields = (
        "subject_visit",
        'ever_sex',
        'lifetime_sex_partners',
        'last_year_partners',
        'more_sex',
        'first_sex',
        'condom',
        'alcohol_sex',)
    radio_fields = {
        "ever_sex": admin.VERTICAL,
        "more_sex": admin.VERTICAL,
        "condom": admin.VERTICAL,
        "alcohol_sex": admin.VERTICAL}
    instructions = [_("<h5>Read to Participant</h5> In this part of the interview,"
                      " I will be asking you some questions about your"
                      " sexual relationships that you might have had,"
                      " and about sexual practices that you might have"
                      " engaged in. Please let me know if you feel "
                      "comfortable answering these questions now or if"
                      " we should move to a different location."
                      " Some of these questions may make you feel uncomfortable;"
                      " however, it is really important for us to get the"
                      " most honest answer that you can give us. Please"
                      " remember that all of your answers are confidential.")]
