from optparse import make_option

from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.models import get_model

from edc_constants.constants import YES

from bhp066.apps.member.constants import BHS, BHS_SCREEN
from bhp066.apps.bcpp_household.models.representative_eligibility import RepresentativeEligibility
from bhp066.apps.member.models.enrollment_checklist import EnrollmentChecklist


class Command(BaseCommand):

    args = ''
    help = 'For Pair 1 data. Create EnrollmentChecklists and set household_structure enrolled '
    'and add Representative Eligibility'

    option_list = BaseCommand.option_list + (
        make_option(
            '--representative-eligibility',
            action='store_true',
            dest='representative-eligibility',
            default=False,
            help=('Auto-create missing RepresentativeEligibility.')),
    )
    option_list += (
        make_option(
            '--enrollment-checklist',
            action='store_true',
            dest='enrollment-checklist',
            default=False,
            help=('Auto-create missing Enrollment Checklist.')),
    )

    def handle(self, *args, **options):
        if options['representative-eligibility']:
            self.create_representative_eligibility()
        elif options['enrollment-checklist']:
            self.create_enrollment_checklist()
        else:
            raise CommandError('Valid options are --representative-eligibility OR --enrollment-checklist.')

    def household_member(self, subject_consent):
        HouseholdMember = get_model('member', 'HouseholdMember')
        try:
            household_member = HouseholdMember.objects.get(
                relation='head',
                household_structure=subject_consent.household_member.household_structure)
        except HouseholdMember.DoesNotExist:
            household_member = subject_consent.household_member
        except MultipleObjectsReturned:
            household_member = HouseholdMember.objects.filter(
                relation='head',
                household_structure=subject_consent.household_member.household_structure)[0]
        return household_member

    def create_representative_eligibility(self):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        n = 0
        print 'auto-creating RepresentativeEligibility'
        subject_consents = SubjectConsent.objects.filter(
            household_member__household_structure__household__plot__map_area__in=['ranaka', 'digawana']).order_by(
                'subject_identifier')
        consent_count = subject_consents.count()
        print 'Found {} consents from ranaka, digawana'.format(consent_count)
        print 'Updating'
        for subject_consent in subject_consents:
            household_member = self.household_member(subject_consent)
            options = dict(
                household_structure=subject_consent.household_member.household_structure,
                auto_filled=True,
                report_datetime=household_member.created,
                aged_over_18=YES,
                household_residency=YES,
                verbal_script=YES)
            try:
                RepresentativeEligibility.objects.get(
                    household_structure=subject_consent.household_member.household_structure)
            except RepresentativeEligibility.DoesNotExist:
                RepresentativeEligibility.objects.create(**options)
                n += 1
        print 'Done. Created {} RepresentativeEligibility'.format(n)

    def create_enrollment_checklist(self):
        SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
        print 'Auto create enrollment checklist if required and save consent to flag household_structure as enrolled'
        subject_consents = SubjectConsent.objects.filter(
            household_member__household_structure__household__plot__map_area__in=['ranaka', 'digawana']).order_by(
                'subject_identifier')
        consent_count = subject_consents.count()
        consents, enrollments = 0, 0
        print 'Found {} consents from ranaka, digawana'.format(consent_count)
        print 'Updating'
        n = 0
        for subject_consent in subject_consents:
            n += 1
            print '  {}/{}'.format(n, consent_count)
            subject_consent.household_member.member_status = BHS_SCREEN
            subject_consent.household_member.household_structure.household.plot.status = 'residential_habitable'
            subject_consent.citizen = 'Yes' if subject_consent.citizen == '2' else subject_consent.citizen
            subject_consent.household_member.eligible_member = True
            try:
                enrollment_checklist = EnrollmentChecklist.objects.get(
                    household_member=subject_consent.household_member)
                subject_consent.household_member.eligible_subject = True
                if enrollment_checklist.citizen == '2':
                    enrollment_checklist.citizen = 'Yes'
                    enrollment_checklist.save_base('citizen')
                subject_consent.household_member.save_base(update_fields=['eligible_member', 'eligible_subject'])
            except EnrollmentChecklist.DoesNotExist:
                try:
                    options = dict(
                        household_member=subject_consent.household_member,
                        report_datetime=subject_consent.created,
                        initials=subject_consent.initials,
                        dob=subject_consent.dob,
                        guardian=subject_consent.is_minor,
                        gender=subject_consent.gender,
                        has_identity=YES,
                        citizen=subject_consent.citizen,
                        legal_marriage=subject_consent.legal_marriage,
                        marriage_certificate=subject_consent.marriage_certificate,
                        part_time_resident=YES,
                        household_residency=YES,
                        literacy=YES,
                        is_eligible=True,
                        auto_filled=True)
                    EnrollmentChecklist.objects.create(**options)
                    enrollments += 1
                except ValidationError as e:
                    print '    Failed to create EnrollmentChecklist for {}. Got {}'.format(subject_consent, str(e))
            subject_consent.household_member.member_status = BHS
            # subject_consent.household_member.save()
            try:
                subject_consent.save()
                consents += 1
            except (ValidationError, IntegrityError) as e:
                print '    Error saving SubjectConsent:   {} {}'.format(subject_consent.subject_identifier, str(e))
        print 'Done. Updated {} SubjectConsents, create {} EnrollmentChecklists'.format(consents, enrollments)
