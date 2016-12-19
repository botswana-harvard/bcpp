from __future__ import print_function

from django.core.management.base import BaseCommand


from bhp066.apps.bcpp_clinic.models import ClinicConsent
from edc_consent.models.consent_type import ConsentType


class Command(BaseCommand):
    help = ('Updates the subject consent version field from \'?\'.')

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        self.resave_clinic_consents(community_name)

    def resave_clinic_consents(self, community_name):
        clinic_consents = ClinicConsent.objects.filter(household_member__household_structure__household__plot__map_area=community_name)
        count = 0
        total = clinic_consents.count()
        print("Updating {} consent versions".format(total))
        for consent in clinic_consents:
            consent.save()
            count += 1
            print ("{0} done out of {1}".format(count, total))
        print("Done.")
