from uuid import uuid4

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.model.models.url_mixin import UrlMixin
from edc_base.utils import formatted_age


def get_uuid():
    return str(uuid4())


class Enrollment(CreateAppointmentsMixin, UrlMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    community = models.CharField(
        max_length=25)

    visit_code = models.CharField(
        max_length=25)

    history = HistoricalRecords()

    def age(self):
        return formatted_age(self.dob, timezone.now().date())
    age.allow_tags = True

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'subject_identifier': self.subject_identifier
            })
        ret = """<a href="{url}" role="button" class="btn btn-sm btn-primary">dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule'
        verbose_name = 'Enrollment'
