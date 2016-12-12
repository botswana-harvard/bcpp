import factory

from datetime import datetime

from subject_visit_factory import SubjectVisitFactory

from bhp066.apps.bcpp_subject.models import MedicalDiagnoses


class MedicalDiagnosesFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MedicalDiagnoses

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
    heart_attack_record = None
    cancer_record = None
    tb_record = None
