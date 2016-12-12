from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import ParticipationForm
from ..models import Participation

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Participation, site=bcpp_subject_admin)
class ParticipationAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ParticipationForm
    fields = (
        "subject_visit",
        "full",
        "participation_type",
    )
    list_display = ('subject_visit', 'full', 'participation_type')
    list_filter = ('subject_visit', 'full', 'participation_type')
    radio_fields = {
        'full': admin.VERTICAL,
        'participation_type': admin.VERTICAL}
