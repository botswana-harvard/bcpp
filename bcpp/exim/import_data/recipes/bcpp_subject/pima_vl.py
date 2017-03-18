import numpy as np

from bcpp_subject.choices import PIMA

# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from .pima_cd4 import reason_not_done, reason_not_done_other

df_drop_columns = ['quota_pk', 'request_code']

df_add_columns = []

df_copy_columns = {'comment': 'reason_not_done'}

df_rename_columns = {
    #'poc_vl_today': 'test_done',
    #'poc_vl_today_other': 'reason_not_done',
    #'poc_today_vl_other_other': 'reason_not_done_other',
    #'pima_id': 'machine_identifier',
    #'poc_vl_value': 'result_value',
    #'time_of_result': 'result_datetime',
    #'vl_value_quatifier': 'quantifier',
    #'time_of_test': 'test_datetime',
}

df_apply_functions = {
    'location': lambda row: common_choices(row['location']),
    'quantifier': lambda row: common_choices(row['quantifier']),
    'easy_of_use': lambda row: common_choices(row['easy_of_use']),
    'test_done': lambda row: common_choices(row['test_done']),
    'reason_not_done_other': lambda row: reason_not_done_other(row),
    'reason_not_done': lambda row: reason_not_done(row),
    'comment': lambda row: np.NaN if row['comment'] in [t[0] for t in PIMA] else row['comment'],
}


m2m_recipes = []

"""
manually created CSV. was full of duplicates.
"""

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.pimavl',
    df_drop_columns=None,
    df_add_columns=None,
    df_copy_columns=None,
    df_rename_columns=None,
    df_apply_functions=None,
    m2m_recipes=m2m_recipes,
))
