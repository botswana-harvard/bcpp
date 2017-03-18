import pandas as pd

from bcpp_subject.subject_helper import SubjectHelper
from bcpp_subject.models import SubjectVisit


"""
SELECT a.id from bhp066.bcpp_subject_subjectvisit as a
left join bcpp_subject_subjectvisit as b on replace(a.id,'-','')=b.id
where substring(b.subject_identifier,1,4)<>'066-';
"""


class CompareSubjectStatus:

    def __init__(self, subject_identifier=None, df=None):
        self.subject_identifier = None
        self.subject_visit = None
        self.df = pd.DataFrame()
        self.sh = None

        self.dataframe = pd.read_csv(
            '/Users/erikvw/Downloads/most_recent_expanded_16mar17.csv',
            low_memory=True)
        self.update(subject_identifier=subject_identifier)

    def update(self, subject_identifier=None):
        self.subject_identifier = subject_identifier
        self.subject_visits = SubjectVisit.objects.filter(
            subject_identifier=subject_identifier).order_by(
                'report_datetime')
        self.subject_visit = self.subject_visits.last()
        self.sh = SubjectHelper(visit=self.subject_visit)
        self.df = self.dataframe[
            self.dataframe['subject_identifier'] == self.subject_identifier]
