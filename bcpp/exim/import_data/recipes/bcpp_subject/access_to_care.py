from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'access_care': lambda row: common_choices(row['access_care']),
    'local_hiv_care': lambda row: common_choices(row['local_hiv_care']),
    'overall_access': lambda row: common_choices(row['overall_access']),
    'emergency_access': lambda row: common_choices(row['emergency_access']),
    'expensive_access': lambda row: common_choices(row['expensive_access']),
    'convenient_access': lambda row: common_choices(row['convenient_access']),
    'whenever_access': lambda row: common_choices(row['whenever_access']),
}

m2m_recipes = [
    M2mRecipe(
        data_model_name='bcpp_subject.accesstocare',
        old_data_model_app_label='bcpp_subject',
        list_model_name='bcpp_subject.medicalcareaccess',
        old_list_model_name='bcpp_list.medicalcareaccess',
        join_lists_on='name')]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.accesstocare',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
