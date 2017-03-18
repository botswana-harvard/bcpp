import csv
import sys
import pandas as pd

from bcpp_subject.models import SubjectVisit
from bcpp_subject.subject_helper import SubjectHelper
from edc_constants.constants import POS, NEG, NAIVE
from bcpp_subject.subject_helper.constants import ON_ART, DEFAULTER


class HivStatus:

    def __init__(self, path=None, sep=None, csv_filename=None):
        if csv_filename:
            self.df = pd.read_csv(csv_filename, low_memory=False)
        else:
            self.df = pd.DataFrame()
            subject_identifiers = []
            subjects = []
            for obj in SubjectVisit.objects.all():
                subject_identifiers.append(obj.subject_identifier)

            subject_identifiers = list(set(subject_identifiers))
            subject_identifiers.sort()
            total = len(subject_identifiers)
            for index, subject_identifier in enumerate(subject_identifiers):
                sys.stdout.write('{}/{}   \r'.format(index + 1, total))
                subjects.append({
                    k: v for k, v in SubjectHelper(
                        subject_identifier=subject_identifier).options.items() if k not in [
                        'baseline', 'current', 'subject_visit']})
            sys.stdout.write('{}/{}   Done\n'.format(index + 1, total))
            self.df = pd.DataFrame(subjects)
            self.df.to_csv(
                path_or_buf=path,
                index=False,
                encoding='utf-8',
                sep=sep or '|',
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                line_terminator='\n',
                escapechar='\\')
            sys.stdout.write('Dataframe exported to {}.\n'.format(path))

    def merge(self, dfB=None, csv_filename=None):
        def convert_sas_date(value):
            raise

        if csv_filename:
            dfB = pd.read_csv(csv_filename, low_memory=False)
            dfB['final_hiv_status'] = dfB[
                'final_hiv_status'].map({1: POS, 0: NEG})
            dfB['final_arv_status'] = dfB[
                'final_arv_status'].map({1: NAIVE, 2: DEFAULTER, 3: ON_ART})
            dfB['base_arv_status'] = dfB[
                'base_arv_status'].map({1: NAIVE, 2: DEFAULTER, 3: ON_ART})
            dfB['consent_date'] = dfB.apply(
                lambda row: convert_sas_date(row['consent_date']))
            dfB['visitdt'] = dfB.apply(
                lambda row: convert_sas_date(row['visitdt']))

        df = pd.merge(
            dfB, self.df, on='subject_identifier', suffixes=['_B', '_A'])
