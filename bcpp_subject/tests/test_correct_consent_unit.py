from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.test import TestCase
from django.utils import timezone

# from bhp066.apps.bcpp_subject.models.signals import update_or_create_registered_subject_on_post_save
from bhp066.apps.member.models.enrollment_checklist import BaseEnrollmentChecklist
from bhp066.apps.bcpp_subject.models.correct_consent import BaseCorrectConsent
from django.core.exceptions import ValidationError


class TestManager(models.Manager):
    def get_by_natural_key(self, pk):
        return self.get(pk=pk)


class TestBase(models.Model):

    first_name = models.CharField(max_length=25, null=True)

    initials = models.CharField(max_length=25, null=True)

    gender = models.CharField(max_length=25, null=True)

    objects = TestManager()

    def natural_key(self):
        return self.pk

    class Meta:
        abstract = True


class Member(TestBase):

    age_in_years = models.IntegerField()

    @property
    def enrollment_checklist(self):
        return Checklist.objects.get(household_member=self)

    class Meta:
        app_label = 'bcpp_subject'


class Checklist(BaseEnrollmentChecklist):

    household_member = models.ForeignKey(Member)

    objects = TestManager()

    def natural_key(self):
        raise

    class Meta:
        app_label = 'bcpp_subject'


class TestBaseConsent(TestBase):

    last_name = models.CharField(max_length=25, null=True)

    guardian_name = models.CharField(max_length=25, null=True)

    witness_name = models.CharField(max_length=25, null=True)

    is_literate = models.CharField(max_length=25, null=True)

    dob = models.DateField(null=True)

    class Meta:
        abstract = True


class Consent(TestBaseConsent):

    household_member = models.ForeignKey(Member)

    class Meta:
        app_label = 'bcpp_subject'


class Correct(BaseCorrectConsent):

    subject_consent = models.ForeignKey(Consent)

    enrollment_checklist = models.ForeignKey(Checklist)

    objects = TestManager()

    def natural_key(self):
        raise

    class Meta:
        app_label = 'bcpp_subject'


class TestCorrectConsent(TestCase):

    def test_update_first_name_changes_initials(self):
        old_first_name = 'BAGGIE'
        new_first_name = 'MAGGIE'
        old_last_name = 'MEAD'
        new_last_name = None
        old_initials = 'BM'
        new_initials = None
        member, checklist, consent, correct = self.update(
            old_first_name, new_first_name,
            old_last_name, new_last_name,
            old_initials, new_initials)
        self.assertEqual(consent.initials, 'MM')
        self.assertEqual(member.initials, 'MM')
        self.assertEqual(checklist.initials, 'MM')
        self.assertEqual(correct.new_initials, None)

    def test_update_initials_match_name_or_raises(self):
        old_first_name = 'MAGGIE'
        new_first_name = None
        old_last_name = 'MEAD'
        new_last_name = None
        old_initials = 'MM'
        new_initials = 'DD'
        self.assertRaises(
            ValidationError,
            self.update,
            old_first_name, new_first_name,
            old_last_name, new_last_name,
            old_initials, new_initials)
        new_initials = 'MXM'
        member, checklist, consent, correct = self.update(
            old_first_name, new_first_name,
            old_last_name, new_last_name,
            old_initials, new_initials)
        self.assertEqual(consent.initials, 'MXM')
        self.assertEqual(member.initials, 'MXM')
        self.assertEqual(checklist.initials, 'MXM')
        self.assertEqual(correct.new_initials, 'MXM')

    def update(self, old_first_name=None, new_first_name=None, old_last_name=None, new_last_name=None,
               old_initials=None, new_initials=None, old_dob=None, new_dob=None):
        old_age = 25 if not old_dob else relativedelta(date.today() - old_dob)
        old_dob = old_dob or timezone.now() - relativedelta(years=old_age)
        member = Member.objects.create(
            first_name=old_first_name,
            initials=old_initials,
            age_in_years=old_age,
        )
        checklist = Checklist.objects.create(
            household_member=member,
            report_datetime=timezone.now(),
            initials=old_initials,
            dob=old_dob,
        )
        consent = Consent.objects.create(
            household_member=member,
            first_name=old_first_name,
            last_name=old_last_name,
            initials=old_initials,
            dob=old_dob,
        )
        self.assertEquals(member.initials, old_initials)
        correct = Correct.objects.create(
            subject_consent=consent,
            enrollment_checklist=checklist,
            old_first_name=old_first_name if new_first_name else None,
            new_first_name=new_first_name,
            old_last_name=old_last_name if new_last_name else None,
            new_last_name=new_last_name,
            old_initials=old_initials if new_initials else None,
            new_initials=new_initials,
            old_dob=old_dob if new_dob else None,
            new_dob=new_dob,
        )
        # call signal
        # update_or_create_registered_subject_on_post_save(Consent, consent, False False)
        consent = Consent.objects.get(pk=consent.pk)
        member = Member.objects.get(pk=member.pk)
        checklist = Checklist.objects.get(pk=member.pk)
        return member, checklist, consent, correct
