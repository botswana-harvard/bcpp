from ..models import HicEnrollment, SubjectReferral


def update_referrals_for_hic(self):
    for hic_enrollment in HicEnrollment.objects.all():
        try:
            bhs_referral_code = SubjectReferral.objects.get(
                subject_visit=hic_enrollment.subject_visit).referral_code
            hic_enrollment.bhs_referral_code = bhs_referral_code
            hic_enrollment.save(update_fields=['bhs_referral_code'])
        except SubjectReferral.DoesNotExist:
            pass
