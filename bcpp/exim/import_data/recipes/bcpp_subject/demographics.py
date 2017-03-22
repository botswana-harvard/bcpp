from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from edc_constants.constants import OTHER, DWTA

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'religion': lambda row: common_choices(row['religion']),
    'ethnic': lambda row: common_choices(row['ethnic']),
    'marital_status': lambda row: common_choices(row['marital_status']),
}


def update_m2m_options(row):
    if row['short_name'] in ['Other', 'other']:
        return OTHER
    elif row['short_name'] in ['Don\'t want to answer']:
        return DWTA
    return row['short_name']

m2m_recipes = [
    M2mRecipe(
        field_name='live_with',
        data_model_name='bcpp_subject.demographics',
        old_data_model_app_label='bcpp_subject',
        list_model_name='bcpp_subject.livewith',
        old_list_model_name='bcpp_list.livewith',
        join_lists_on='short_name',
        df_apply_functions={'short_name': lambda row: update_m2m_options(row)}
    )
]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.demographics',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
