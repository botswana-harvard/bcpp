from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import NonPregnancyForm
from ..models import NonPregnancy

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(NonPregnancy, site=bcpp_subject_admin)
class NonPregnancyAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = NonPregnancyForm
    fields = (
        "subject_visit",
        'last_birth',
        'anc_last_pregnancy',
        'hiv_last_pregnancy',
        'preg_arv',
        'more_children'
    )
    radio_fields = {"more_children": admin.VERTICAL,
                    "anc_last_pregnancy": admin.VERTICAL,
                    "hiv_last_pregnancy": admin.VERTICAL,
                    "preg_arv": admin.VERTICAL}
