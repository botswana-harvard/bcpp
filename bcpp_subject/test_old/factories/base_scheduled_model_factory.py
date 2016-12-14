import factory

from .subject_visit_factory import SubjectVisitFactory


class BaseScheduledModelFactory(factory.DjangoModelFactory):
    ABSTRACT_FACTORY = True

    subject_visit = factory.SubFactory(SubjectVisitFactory)
