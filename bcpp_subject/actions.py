from .models import SubjectReferral


def update_referrals(modeladmin, request, queryset):
    for obj in queryset:
        try:
            bhs_referral_code = SubjectReferral.objects.get(subject_visit=obj.subject_visit).referral_code
            obj.bhs_referral_code = bhs_referral_code
            obj.save(update_fields=['bhs_referral_code'])
        except SubjectReferral.DoesNotExist:
            pass
update_referrals.short_description = "Update selected referrals"
