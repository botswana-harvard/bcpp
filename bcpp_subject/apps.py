from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'

    def ready(self):
        from bcpp_subject.models.signals import (
            subject_consent_on_post_save, update_or_create_registered_subject_on_post_save,
            update_subject_referral_on_post_save)
