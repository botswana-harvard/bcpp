import numpy as np
import pandas as pd

from edc_constants.constants import OTHER, NO, YES

from bcpp_subject.choices import PIMA

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices


def reason_not_done(row):
    choices = ['Participant Declined',
               'Multiple PIMA malfunction', 'Failed Blood Collection']
    if pd.isnull(row['reason_not_done']):
        return np.NaN
    elif (row['reason_not_done'] not in choices and row['test_done'] == NO):
        return OTHER
    elif (row['reason_not_done'] not in choices and row['test_done'] == YES):
        return np.NaN
    return row['reason_not_done']


def reason_not_done_other(row):
    choices = ['Participant Declined',
               'Multiple PIMA malfunction', 'Failed Blood Collection']
    if row['test_done'] == YES and pd.notnull(row['result_value']):
        return np.NaN
    elif pd.notnull(row['reason_not_done_other']):
        return row['reason_not_done_other']
    elif (row['reason_not_done'] not in choices and row['test_done'] == NO):
        return row['reason_not_done']
    return np.NaN


df_drop_columns = []

df_add_columns = []

df_copy_columns = {'comment': 'pima_today_other'}

df_rename_columns = {
    'pima_today': 'test_done',
    'pima_today_other': 'reason_not_done',
    'pima_today_other_other': 'reason_not_done_other',
    'pima_id': 'machine_identifier',
    'cd4_value': 'result_value',
    'cd4_datetime': 'result_datetime',
}

df_apply_functions = {
    'test_done': lambda row: common_choices(row['test_done']),
    'reason_not_done_other': lambda row: reason_not_done_other(row),
    'reason_not_done': lambda row: reason_not_done(row),
    'comment': lambda row: np.NaN if row['comment'] in [t[0] for t in PIMA] else row['comment'],
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.pimacd4',
    old_model_name='bcpp_subject.pima',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_copy_columns=df_copy_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
