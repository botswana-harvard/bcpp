from django.urls import reverse
from django.test.testcases import TestCase, tag

from ..navbars import navbars


@tag('1')
class TestUrls(TestCase):

    def test_admin_urls(self):
        self.assertEqual(reverse('plot_admin:index'), '/admin/')
        self.assertEqual(reverse('household_admin:index'), '/admin/')
        self.assertEqual(reverse('member_admin:index'), '/admin/')
        self.assertEqual(reverse('bcpp_subject_admin:index'), '/admin/')

    def test_home_urls(self):
        self.assertEqual(reverse('edc_consent:home_url'), '/edc_consent/')
        self.assertEqual(reverse('edc_device:home_url'), '/edc_device/')
        self.assertEqual(
            reverse('edc_lab_dashboard:home_url'), '/edc_lab_dashboard/')
        self.assertEqual(reverse('edc_label:home_url'), '/edc_label/')
        self.assertEqual(reverse('edc_map:home_url'), '/edc_map/')
        self.assertEqual(reverse('bcpp_report:home_url'), '/bcpp_report/')
        self.assertEqual(reverse('edc_metadata:home_url'), '/edc_metadata/')

        self.assertEqual(reverse('edc_protocol:home_url'), '/edc_protocol/')
        self.assertEqual(
            reverse('edc_registration:home_url'), '/edc_registration/')
        self.assertEqual(reverse('edc_sync:home_url'), '/edc_sync/')
        self.assertEqual(reverse('edc_visit_schedule:home_url'),
                         '/edc_visit_schedule/')

    def test_navbar_urls(self):
        for cat, navbar_items in navbars.items():
            for navbar_item in navbar_items:
                print(
                    f'{cat} {navbar_item.app_config_name}:{navbar_item.app_config_attr}')
                print(reverse(f'{navbar_item.url_name}'))
