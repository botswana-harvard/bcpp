from django.core.management.base import BaseCommand, CommandError

from edc_constants.constants import NEG, YES, NO

from household.constants import BASELINE_SURVEY
from bcpp_subject.models import SubjectVisit, SubjectLocator, ResidencyMobility, HicEnrollment, SubjectConsent
from bcpp_subject.subject_status_helper import SubjectStatusHelper


def create_hic_enrollment(self, n, created, verbose, subject_consent, hic_enrollment):
    try:
        subject_visit = SubjectVisit.objects.get(
            household_member=subject_consent.household_member,
            appointment__visit_definition__time_point=0)
    except SubjectVisit.DoesNotExist:
        print('{}.   missing SubjectVisit'.format(n))
    try:
        residency_and_mobility = ResidencyMobility.objects.get(
            subject_visit=subject_visit)
    except ResidencyMobility.DoesNotExist:
        print('{}.   missing ResidencyMobility'.format(n))
    if residency_and_mobility.modified.year == 2013:
        # this question has flipped after pair 1
        residency_and_mobility.intend_residency = YES if(
            residency_and_mobility.intend_residency == NO) else NO
        residency_and_mobility.save()
    try:
        subject_locator = SubjectLocator.objects.get(
            subject_visit=subject_visit)
    except SubjectLocator.DoesNotExist:
        print('{}.   missing SubjectLocator'.format(n))
    if (SubjectStatusHelper(subject_visit).hiv_result == NEG and
            residency_and_mobility.permanent_resident == YES and
            residency_and_mobility.intend_residency == NO and
            subject_locator.may_follow_up == YES):
        hic_enrollment = HicEnrollment.objects.create(
            hic_permission=YES,
            subject_visit=subject_visit,
            permanent_resident=True,
            intend_residency=True,
            hiv_status_today=NEG,
            dob=subject_consent.dob,
            citizen_or_spouse=True,
            locator_information=True,
            consent_datetime=subject_consent.consent_datetime
        )
        created += 1
        if verbose:
            print('{}. created {}'.format(n, hic_enrollment))
    else:
        print('    not eligible hiv={}, resident={}, moving={}, follow={}'.format(
            SubjectStatusHelper(subject_visit).hiv_result,
            residency_and_mobility.permanent_resident,
            residency_and_mobility.intend_residency,
            subject_locator.may_follow_up))


def hic_for_consents(verbose, subject_consents, total_consents):
    created = 0
    enrolled = 0
    n = 0
    for subject_consent in subject_consents:
        try:
            hic_enrollment = HicEnrollment.objects.get(
                subject_visit__household_member=subject_consent.household_member)
            enrolled += 1
            print('{}. already enrolled'.format(n))
        except HicEnrollment.DoesNotExist:
            create_hic_enrollment(n, created, verbose, subject_consent, hic_enrollment)
        n += 1
    print('Reviewed {} consents from Pair 1. Created {} HIC Enrollment forms. {} already enrolled'.format(
        total_consents, created, enrolled))


class Command(BaseCommand):

    args = 'verbose update_resmob (only do this ONCE!!)'
    help = 'generate hic enrollment form for pair 1 eligible members.'

    def handle(self, *args, **options):
        if HicEnrollment.objects.filter(
                subject_visit__household_member__household_structure__household__plot__map_area__in=[
                    'ranaka', 'digawana']).count() != 0:
            raise CommandError('This command has already been run and cannot be run twice.')
        try:
            verbose = args[0]
        except IndexError:
            verbose = False
        subject_consents = SubjectConsent.objects.filter(
            household_member__household_structure__household__plot__map_area__in=['ranaka', 'digawana'],
            household_member__household_structure__survey__survey_slug=BASELINE_SURVEY)
        total_consents = subject_consents.count()
        hic_for_consents(verbose, subject_consents, total_consents)
