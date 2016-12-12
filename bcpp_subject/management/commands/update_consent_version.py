from __future__ import print_function

import sys

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from bhp066.apps.bcpp_subject.models import SubjectConsent
from edc_consent.models.consent_type import ConsentType


class Command(BaseCommand):
    help = ('Updates the subject consent version field from \'?\'.')

    def handle(self, *args, **options):
        self.resave_consents()

    def resave_consents(self):
        consents = SubjectConsent.objects.filter(version='4')
        count = 0
        total = consents.count()
        print("Updating {} consents where version == \'4\' to version 5 ".format(total))
        for consent in consents:
            consent.save()
            count += 1
            print ("{0} done out of {1}".format(count, total))
#         sys.stdout.flush()
#         dct = {}
#         for consent_type in ConsentType.objects.all():
#             dct[consent_type.version] = []
#         for consent in consents:
#             count += 1
#             consent_type = ConsentType.objects.get_by_consent_datetime(
#                 SubjectConsent, consent.consent_datetime)
#             consent.version = consent_type.version
#             dct[consent.version].append(consent.pk)
#             print('{} / {} \r'.format(count, total), end="")
#             sys.stdout.flush()
#         for version, pks in dct.iteritems():
#             print("   {} consents set to version {} ".format(len(pks), version))
#             SubjectConsent.objects.filter(pk__in=pks).update(version=version)
        print("Done.")
