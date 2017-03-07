from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, tag

from bcpp_subject.tests.test_mixins import SubjectMixin
from survey.site_surveys import site_surveys
from pprint import pprint
from bcpp.views import HomeView
from plot.views.listboard_view import ListBoardView as PlotListBoardView


@tag('erik')
class TestViews(SubjectMixin, TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='erik', email='erik@…', password='top_secret')
        self.client.force_login(self.user)
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=site_surveys.get_survey_schedules()[0],
            make_hoh=False)
        first_household_member = self.add_household_member(
            household_structure=household_structure)
        self.subject_consent = self.add_subject_consent(first_household_member)

    def test_home(self):
        response = self.client.get(reverse('home_url'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], HomeView)

    def test_listboard_plot(self):
        response = self.client.get(reverse('plot:listboard_url', kwargs={}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], PlotListBoardView)

    def test_listboard_member(self):
        response = self.client.get(reverse('member:listboard_url', kwargs={}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], HomeView)

    def test_listboard_household(self):
        response = self.client.get(
            reverse('household:listboard_url', kwargs={}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], HomeView)

    def test_listboard_enumeration(self):
        response = self.client.get(
            reverse('enumeration:listboard_url', kwargs={}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], HomeView)

    def test_listboard_bcpp_subject(self):
        response = self.client.get(reverse('bcpp_subject:listboard_url'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['view'], HomeView)
