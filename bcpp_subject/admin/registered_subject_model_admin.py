from django.contrib import admin

from edc_registration.admin import RegisteredSubjectModelAdminMixin


class RegisteredSubjectModelAdmin (RegisteredSubjectModelAdminMixin, admin.ModelAdmin):

    """ModelAdmin subclass for models with a ForeignKey to 'registered_subject'"""
    pass
