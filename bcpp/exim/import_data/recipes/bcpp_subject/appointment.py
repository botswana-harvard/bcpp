import pandas as pd
import sys

from edc_appointment.constants import SCHEDULED_APPT
from edc_pdutils.model_to_dataframe import ModelToDataFrame

from member.models import HouseholdMember
from bcpp_subject.constants import T0, T1, T2, T3, C0

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ...exceptions import ImportDataError
from ..household.household_structure import survey_schedule


def visit_schedule_name(row):
    """This will need to consider the Survey schedule name.
    """
    if row['visit_definition_id'] == '3138f9da-0e57-4d0a-8afd-761f096203d6':
        return 'visit_schedule'
    elif row['visit_definition_id'] == 'dab10682-e7c8-11e3-8dc4-a82066234239':
        return 'visit_schedule'
    elif row['visit_definition_id'] == '6082137a-9a30-4e59-9755-36c4f22f29cc':
        return 'visit_schedule'
    elif row['visit_definition_id'] == 'a55f212a-d357-4fe2-a334-dd9fcf8d17e0':
        return 'visit_schedule'


def schedule_name(row):
    if row['visit_definition_id'] == '3138f9da-0e57-4d0a-8afd-761f096203d6':
        return 'cln_schedule'
    elif row['visit_definition_id'] == 'dab10682-e7c8-11e3-8dc4-a82066234239':
        return 'bhs_schedule'
    elif row['visit_definition_id'] == '6082137a-9a30-4e59-9755-36c4f22f29cc':
        return 'ahs_schedule'
    elif row['visit_definition_id'] == 'a55f212a-d357-4fe2-a334-dd9fcf8d17e0':
        return 'ahs_schedule'


def visit_code(row):
    if row['visit_definition_id'] == '3138f9da-0e57-4d0a-8afd-761f096203d6':
        return C0
    elif row['visit_definition_id'] == 'dab10682-e7c8-11e3-8dc4-a82066234239':
        return T0
    elif row['visit_definition_id'] == '6082137a-9a30-4e59-9755-36c4f22f29cc':
        return T1
    elif row['visit_definition_id'] == 'a55f212a-d357-4fe2-a334-dd9fcf8d17e0':
        return T2


def appt_type(row):
    if visit_code(row) == 'C0':
        return 'clinic'
    elif row['appt_type'] == 'default':
        return 'home'
    return row['appt_type']


def timepoint(row):
    if visit_code(row) in [C0, T0]:
        return 0
    elif visit_code(row) == T1:
        return 1
    elif visit_code(row) == T2:
        return 2
    elif visit_code(row) == T3:
        return 3
    raise ImportDataError('Invalid row for timepoint')


df_drop_columns = [
    'visit_definition_id',
    'contact_tel',
    'best_appt_datetime',
    'contact_count',
    'dashboard_type',
    'study_site_id']

df_rename_columns = {
    'registered_subject_id': 'subject_identifier',  # temp rename
}

df_add_columns = [
    'survey_schedule',
    'visit_schedule_name',
    'schedule_name',
    'visit_code',
    'household_member_id']

df_apply_functions = {
    'visit_code': lambda row: visit_code(row),
    'schedule_name': lambda row: schedule_name(row),
    'visit_schedule_name': lambda row: visit_schedule_name(row),
    'survey_schedule': lambda row: survey_schedule(row),
    'appt_type': lambda row: appt_type(row),
    'timepoint': lambda row: timepoint(row),
    'appt_reason': lambda row: SCHEDULED_APPT,
    'is_confirmed': lambda row: 1 if row['is_confirmed'] is True else 0,
}


class AppointmentRecipe(ModelRecipe):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subject_visit_df = pd.DataFrame()
        self._household_member_df = pd.DataFrame()
        self.merged = False

    @property
    def subject_visit_df(self):
        if self._subject_visit_df.empty:
            recipe = site_recipes.recipes.get('bcpp_subject.subjectvisit')
            obj = recipe.import_csv_class(recipe=recipe)
            self._subject_visit_df = obj.df
        return self._subject_visit_df

#     @property
#     def household_member_df(self):
#         if self._household_member_df.empty:
#             pd.
#             obj = ModelToDataFrame(model=HouseholdMember)
#             self._household_member_df = obj.df
#         return self._household_member_df

    @property
    def df(self):
        if self._df.empty:
            super().df
            if not self.merged:
                sys.stdout.write('merging with subject_visit ...\r')
                cols = list(set(list(self._df.columns)))
                cols.sort()
                df = pd.merge(self.subject_visit_df, self._df, left_on='appointment_id',
                              right_on='id', how='left', suffixes=['_visit', ''])
                df = df.drop(['household_member_id'], axis=1)
                df = df.rename(
                    columns={'household_member_id_visit': 'household_member_id'})
                self._df = df[cols].copy()
                self.merged = True
                sys.stdout.write('merging with subject_visit ... Done\n')
                # merge in household_member_id from subject_visit
        return self._df

site_recipes.register(AppointmentRecipe(
    model_name='bcpp_subject.appointment',
    old_model_name='appointment.appointment',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
