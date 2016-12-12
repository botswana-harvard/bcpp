from edc_identifier.subject.classes import SubjectIdentifier


class ConsentedSubjectIdentifier(SubjectIdentifier):
    """ Manages identifiers for subject consents.

    Note, registered subject is created on a signal in bhp_subject by the consent
    model (which is a subclass of BaseSubject)."""

    def __init__(self, site_code, using=None):
        super(ConsentedSubjectIdentifier, self).__init__(site_code=site_code, using=using)
