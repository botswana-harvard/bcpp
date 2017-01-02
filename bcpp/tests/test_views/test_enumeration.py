from django.test import TestCase, tag

from member.tests.test_mixins import MemberMixin
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.urls.base import reverse

from enumeration.views import DashboardView


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
        print(response.context_data)
