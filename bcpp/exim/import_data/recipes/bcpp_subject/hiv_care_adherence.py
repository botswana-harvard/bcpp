# from edc_constants.constants import DWTA, NO

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'why_no_arv': lambda row: common_choices(row['why_no_arv']),
    'medical_care': lambda row: common_choices(row['medical_care']),
    'no_medical_care': lambda row: common_choices(row['no_medical_care']),
    'ever_recommended_arv': lambda row: common_choices(row['ever_recommended_arv']),
    'arv_stop': lambda row: common_choices(row['arv_stop']),
    'adherence_4_day': lambda row: common_choices(row['adherence_4_day']),
    'adherence_4_wk': lambda row: common_choices(row['adherence_4_wk']),
    # 'ever_taken_arv': lambda row: NO if row['ever_taken_arv'] == DWTA else row['ever_taken_arv'],
    # 'on_arv': lambda row: NO if row['on_arv'] == DWTA else row['on_arv'],
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivcareadherence',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
