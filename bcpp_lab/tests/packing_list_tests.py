from datetime import datetime

from edc.lab.lab_profile.classes import site_lab_profiles

from bhp066.apps.bcpp_lab.models import AliquotType, Panel
from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from bhp066.apps.bcpp_subject.tests.base_scheduled_model_test_case import BaseScheduledModelTestCase
from bhp066.apps.bcpp_subject.tests.factories import SubjectLocatorFactory, SubjectReferralFactory


from ..models import Aliquot, PackingListItem
from .factories import PackingListFactory


class PackingListTests(BaseScheduledModelTestCase):

    community = 'test_community8'
    site_code = '11'

    def startup(self):
        super(PackingListTests, self).startup()
        SubjectLocatorFactory(subject_visit=self.subject_visit_male)
        SubjectLocatorFactory(subject_visit=self.subject_visit_female)

    def test_create_aliquot_on_receive(self):
        """Asserts packing list items are created by the packing list."""
        self.startup()
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        subject_requisition = SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_annual,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        # receive
        lab_profile = site_lab_profiles.get(subject_requisition._meta.object_name)
        receive = lab_profile().receive(subject_requisition)
        identifiers = '\n'.join([a.aliquot_identifier for a in Aliquot.objects.filter(receive=receive)])
        packing_list = PackingListFactory(list_items=identifiers)
        self.assertGreater(PackingListItem.objects.all().count(), 0)
        for identifier in identifiers:
            self.assertEquals(PackingListItem.objects.get(packing_list=packing_list, item_reference=identifier))
        packing_list = PackingListFactory(list_items=identifiers)
        for identifier in identifiers:
            self.assertEquals(PackingListItem.objects.get(packing_list=packing_list, item_reference=identifier))
