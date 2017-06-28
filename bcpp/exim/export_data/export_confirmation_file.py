import os
import json

from django.apps import apps as django_apps
from django.db.models import Q
from datetime import datetime

from bcpp_subject.models import SubjectVisit, SubjectConsent
from bcpp_subject.sync_models import sync_models
from bcpp_subject.models.model_mixins import CrfModelMixin


class MismatchVerification(Exception):
    pass


class InvalidFilename(Exception):
    pass


class ConfirmationFile:

    def __init__(self, filename=None):
        self.filename = filename
        if not self.filename:
            raise InvalidFilename(f'Filename cannot be {self.filename}.')
        self.data = self.read()

    def read(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data

    def write(self, data=None):
        with open(self.filename, 'w') as f:
            json.dump(data, f)


class ExportConfirmationFile:

    file_writer = ConfirmationFile

    def __init__(self, survey=None,
                 subject_identifiers=None, community=None, verbose=None,
                 start_date=None, end_date=None):
        self.survey = survey
        self.subject_identifiers = subject_identifiers
        self.community = community
        self.edc_sync_file_app = django_apps.get_app_configs('edc_sync_files')
        self.verbose = verbose
        self.start_date = start_date
        self.end_date = end_date

    def subject_visits(self):
        subject_visits = SubjectVisit.objects.filter(
            Q(created__range=(self.start_date, self.end_date))
            | Q(subject_identifier__in=self.subject_identifiers))
        return subject_visits

    def create_subject_consents_file(self):
        filename = '{}_consents_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        filename = os.path.join(
            self.edc_sync_file_app.outgoing_folder, filename)
        data = []
        for subject_visit in self.subject_visits():
            subject_consent = SubjectConsent.objects.get(
                household_member=subject_visit.household_member)
            consent_filter = (
                subject_consent.subject_identifier,
                subject_consent.version,
                str(subject_consent.household_member.internal_identifier),
                subject_consent.household_member.household_structure.survey_schedule,
                subject_consent.household_member.household_structure.household.household_identifier,
                subject_consent.household_member.household_structure.household.plot.plot_identifier)
            data.append(
                {str(SubjectConsent._meta.label_lower): consent_filter})
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))

    def create_subjectvisits_file(self):
        data = []
        for visit in self.subject_visits():
            data.append(
                {str(SubjectVisit._meta.label_lower): visit.natural_key()})
        app = django_apps.get_app_configs('edc_sync_reports')
        filename = '{}_visits_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        filename = os.path.join(app.reports, filename)
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))

    def is_ignored(self, label_lower):
        skip_models = [
            'bcpp_subject.subjectconsent', 'bcpp_subject.correctconsent']
        if not ('historical' in label_lower and label_lower in skip_models):
            return True
        return False

    def crfs_file(self):
        data = []
        model_label_lowers = [
            label for label in sync_models if not self.is_ignored(label)]
        for subject_identifier in self.subject_identifiers:
            visit = SubjectVisit.objects.get(
                survey=self.survey,
                subject_identifier=subject_identifier)
            temp_data = []
            for label_lower in model_label_lowers:
                model = django_apps.get_model(*label_lower.split('.'))
                if issubclass(model, CrfModelMixin):
                    try:
                        obj = model.objects.get(subject_visit=visit)
                    except model.DoesNotExist:
                        pass
                else:
                    try:
                        obj = model.objects.get(
                            subject_identifier=visit.subject_identifier)
                    except model.DoesNotExist:
                        print(model)
                if obj:
                    temp_data.append(
                        dict({str(model._meta.label_lower): obj.natural_key()}))
            data.append(temp_data)
        filename = '{}_consents_data-{}.json'.format(
            self.community, datetime.today().strftime("%Y%m%d%H%m"))
        filename = os.path.join(self.edc_sync_file_app.outgoing_folder, filename)
        self.file_write(filename=filename).write(data=data)
        if self.verbose:
            print("Created {} with {}".format(filename, len(data)))
