from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from edc_constants.constants import OTHER

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'heart_attack_record': lambda row: common_choices(row['heart_attack_record']),
    'cancer_record': lambda row: common_choices(row['cancer_record']),
    'tb_record': lambda row: common_choices(row['tb_record']),
}


def update_m2m_options(row):
    if row['short_name'] == 'Heart Disease':
        return 'heart_disease'
    elif row['short_name'] == 'Cancer':
        return 'cancer'
    elif row['short_name'] == 'Other':
        return OTHER
    return row['short_name']

m2m_recipes = [
    M2mRecipe(
        field_name='diagnoses',
        data_model_name='bcpp_subject.medicaldiagnoses',
        old_data_model_app_label='bcpp_subject',
        list_model_name='bcpp_subject.diagnoses',
        old_list_model_name='bcpp_list.diagnoses',
        join_lists_on='short_name',
        df_apply_functions={'short_name': lambda row: update_m2m_options(row)}
    )
]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.medicaldiagnoses',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
