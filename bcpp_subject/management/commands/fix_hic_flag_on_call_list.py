from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from edc_constants.constants import YES


class Command(BaseCommand):

    args = 'label (from call list e.g. t1-prep)'
    help = 'manually update HIC flag on call list'

    def handle(self, *args, **options):
        try:
            label = args[0]
        except IndexError:
            CommandError('Expected a label.')
        CallList = get_model('bcpp_subject', 'CallList')
        HicEnrollment = get_model('bcpp_subject', 'HicEnrollment')

        hic_enrollments = HicEnrollment.objects.filter(
            subject_visit__household_member__household_structure__household__plot__map_area__in=[
                'ranaka', 'digawana'],
            hic_permission=YES)
        total = hic_enrollments.count()
        n = 0
        print 'Found {} Hic Enrollments'.format(total)
        for hic_enrollment in hic_enrollments:
            try:
                internal_identifier = hic_enrollment.subject_visit.household_member.internal_identifier
                call_list = CallList.objects.get(
                    household_member__internal_identifier=internal_identifier,
                    label=label)
                call_list.hic = True
                call_list.hic_datetime = hic_enrollment.report_datetime
                call_list.save_base(update_fields=['hic', 'hic_datetime'])
                n += 1
            except CallList.DoesNotExist:
                print (
                    '    skipping, not in call list {} (permission={})'
                    ''.format(hic_enrollment, hic_enrollment.hic_permission))
        print ('Done. Update {} rows in CallList for {} Hic Enrollments with call list label'
               ' {}.'.format(n, total, label))
