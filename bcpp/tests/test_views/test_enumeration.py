from django.test import TestCase, tag

from member.tests.test_mixins import MemberMixin
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.urls.base import reverse

from enumeration.views import DashboardView, EnumerationView


class TestEnumeration(MemberMixin, TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='erik')
        self.household_structure = self.make_household_ready_for_enumeration(make_hoh=False)

    def test_dashboard_view(self):
        url = reverse('enumeration:dashboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier,
            survey=self.household_structure.survey))
        request = self.factory.get(url)
        request.user = self.user
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view2(self):
        url = reverse('enumeration:dashboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier,
            survey=self.household_structure.survey))
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view1(self):
        url = reverse('enumeration:listboard_url')
        request = self.factory.get(url)
        request.user = self.user
        response = EnumerationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view2(self):
        url = reverse('enumeration:listboard_url', kwargs=dict(page=1))
        request = self.factory.get(url)
        request.user = self.user
        response = EnumerationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view3(self):
        url = reverse('enumeration:listboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier))
        request = self.factory.get(url)
        request.user = self.user
        response = EnumerationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view4(self):
        url = reverse('enumeration:listboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier,
            survey=self.household_structure.survey))
        request = self.factory.get(url)
        request.user = self.user
        response = EnumerationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view5(self):
        url = reverse('enumeration:listboard_url', kwargs=dict(
            plot_identifier=self.household_structure.household.plot.plot_identifier))
        request = self.factory.get(url)
        request.user = self.user
        response = EnumerationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
