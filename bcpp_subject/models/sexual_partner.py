from django.db import models

from edc_base.model.models import HistoricalRecords

from .model_mixins import CrfModelMixin, CrfModelManager, SexualPartnerMixin


class RecentPartner (SexualPartnerMixin, CrfModelMixin):
    """A model completed by the user on the participant's recent sexual behaviour."""

    first_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.first_partner_arm = self.get_partner_arm()
        super(RecentPartner, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Recent Partner - 12 Months"
        verbose_name_plural = "Recent Partner - 12 Months"


class SecondPartner (SexualPartnerMixin, CrfModelMixin):
    """A model completed by the user on the participant's recent sexual behaviour."""

    second_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.second_partner_arm = self.get_partner_arm()
        super(SecondPartner, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Second Partner - 12 Months"
        verbose_name_plural = "Second Partner - 12 Months"


class ThirdPartner (SexualPartnerMixin, CrfModelMixin):
    """A model completed by the user on the participant's recent sexual behaviour."""

    third_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.third_partner_arm = self.get_partner_arm()
        super(ThirdPartner, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Third Partner - 12 Months"
        verbose_name_plural = "Third Partner - 12 Months"
