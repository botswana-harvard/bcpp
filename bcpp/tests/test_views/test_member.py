from django.test import TestCase

from member.tests.test_mixins import MemberMixin
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from django.urls.base import reverse

from member.views import ListBoardView


class TestMember(MemberMixin, TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='erik')
        self.household_structure = self.make_household_ready_for_enumeration(make_hoh=False)

    def test_list_view1(self):
        url = reverse('member:listboard_url')
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view2(self):
        url = reverse('member:listboard_url', kwargs=dict(page=1))
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view3(self):
        url = reverse('member:listboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier))
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view4(self):
        url = reverse('member:listboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier,
            survey=self.household_structure.survey))
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view5(self):
        url = reverse('member:listboard_url', kwargs=dict(
            plot_identifier=self.household_structure.household.plot.plot_identifier))
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_list_view6(self):
        url = reverse('member:listboard_url', kwargs=dict(
            household_identifier=self.household_structure.household.household_identifier,
            survey=self.household_structure.survey, page=1))
        request = self.factory.get(url)
        request.user = self.user
        response = ListBoardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
