from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        group = Group.objects.get(name='field_research_assistant')
        for permission in Permission.objects.filter(
                content_type__app_label='bcpp_subject',
                content_type__model='SubjectConsent',
                codename__icontains='subjectconsentextended').exclude(codename__startswith='delete'):
            group.permissions.add(permission)
