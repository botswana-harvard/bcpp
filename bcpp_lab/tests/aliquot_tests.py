from datetime import datetime

from edc.lab.lab_requisition.actions import flag_as_received
from edc.lab.lab_profile.classes import site_lab_profiles

from bhp066.apps.bcpp_lab.models import AliquotType, Panel, Receive
from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from bhp066.apps.bcpp_subject.tests.base_scheduled_model_test_case import BaseScheduledModelTestCase
from bhp066.apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory

from ..models import Aliquot


class TestAliquots(BaseScheduledModelTestCase):

    community = 'test_community8'
    site_code = '11'

    def startup(self):
        super(TestAliquots, self).startup()
        SubjectLocatorFactory(subject_visit=self.subject_visit_male)
        SubjectLocatorFactory(subject_visit=self.subject_visit_female)

    def test_create_aliquot_on_receive(self):
        """Asserts a primary aliquot is created on receiving a requisition."""
        self.startup()
        panel = Panel.objects.get(name='Microtube')
        subject_requisition = SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        # receive
        lab_profile = site_lab_profiles.get(subject_requisition._meta.object_name)
        receive = lab_profile().receive(subject_requisition)
        # assert primary aliquot
        try:
            Aliquot.objects.get(receive=receive)
        except Aliquot.DoesNotExist as e:
            self.fail(str(e))

    def test_create_aliquot_on_receive_action(self):
        """Asserts a primary aliquot is created on receiving a requisition (using the action func)."""
        self.startup()
        panel = Panel.objects.get(name='Microtube')
        subject_requisition = SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        self.assertEquals(Aliquot.objects.all().count(), 0)
        # receive using the action
        flag_as_received(None, None, [subject_requisition])
        receive = Receive.objects.get(requisition_identifier=subject_requisition.requisition_identifier)
        # assert primary aliquot
        try:
            Aliquot.objects.all()[0]
        except IndexError:
            self.fail(str('No Aliquots created after receive'))
        try:
            Aliquot.objects.get(receive=receive)
        except Aliquot.DoesNotExist as e:
            self.fail(str(e))
