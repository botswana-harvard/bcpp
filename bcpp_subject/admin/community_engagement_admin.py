from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import CommunityEngagementForm
from ..models import CommunityEngagement

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CommunityEngagement, site=bcpp_subject_admin)
class CommunityEngagementAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CommunityEngagementForm
    fields = (
        "subject_visit",
        'community_engagement',
        'vote_engagement',
        'problems_engagement',
        'problems_engagement_other',
        'solve_engagement',)
    radio_fields = {
        "community_engagement": admin.VERTICAL,
        "vote_engagement": admin.VERTICAL,
        "solve_engagement": admin.VERTICAL, }
    filter_horizontal = ('problems_engagement',)
