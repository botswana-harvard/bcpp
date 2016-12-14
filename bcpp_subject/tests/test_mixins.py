from model_mommy import mommy

from edc_base.test_mixins import AddVisitMixin, ReferenceDateMixin, CompleteCrfsMixin, LoadListDataMixin

from bcpp_subject.list_data import list_data


class SubjectTestMixin(CompleteCrfsMixin, AddVisitMixin, LoadListDataMixin):

    list_data = list_data


class SubjectMixin(ReferenceDateMixin, SubjectTestMixin):
    """Creates a POS mother."""
    def setUp(self):
        super(SubjectMixin, self).setUp()
        self.study_site = '40'

    def make_new_consented_subject(self):
        self.subject_eligibility = self.make_eligibility()
        self.subject_consent = self.make_consent()
        self.subject_identifier = self.subject_consent.subject_identifier

    def make_consent(self):
        return mommy.make_recipe(
            'bcpp_subject.subjectconsent',
            consent_datetime=self.test_mixin_reference_datetime,
            subject_eligibility_reference=self.subject_eligibility.reference)

    def make_positive_subject(self, **options):
        """Make a POS mother LMP 25wks with POS result with evidence (no recent or rapid test)."""
        self.make_new_consented_subject()
        report_datetime = options.get('report_datetime', self.test_mixin_reference_datetime)

    def make_negative_subject(self, **options):
        """Make a NEG mother LMP 25wks with NEG by current, recent or rapid."""
        self.make_new_consented_subject()
        report_datetime = options.get('report_datetime', self.test_mixin_reference_datetime)
