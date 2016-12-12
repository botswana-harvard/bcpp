from django.core.management.base import BaseCommand
from django.db.models import get_model


class Command(BaseCommand):

    args = ''
    help = 'resaves bcpp_subject.subject_referral and prints appt if changed.'

    def handle(self, *args, **options):
        changed = 0
        SubjectReferral = get_model('bcpp_subject', 'SubjectReferral')
        for subject_referral in SubjectReferral.objects.all():
            referral_appt_date = subject_referral.referral_appt_date
            # print subject_referral
            subject_referral.save()
            if referral_appt_date != subject_referral.referral_appt_date:
                changed += 1
                print '  {} {}'.format(subject_referral.referral_appt_date, referral_appt_date)
        print 'Resaved {} referrals. {} referrals changed.'.format(SubjectReferral.objects.all().count(), changed)
