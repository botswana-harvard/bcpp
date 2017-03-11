from edc_constants.constants import DWTA

from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


m2m_recipes = [
    M2mRecipe(
        data_model_name='member.householdinfo',
        old_data_model_app_label='bcpp_household_member',
        list_model_name='member.electricalappliances',
        old_list_model_name='bcpp_list.electricalappliances',
        join_lists_on='name'),
    M2mRecipe(
        data_model_name='member.householdinfo',
        old_data_model_app_label='bcpp_household_member',
        list_model_name='member.transportmode',
        old_list_model_name='bcpp_list.transportmode')]

df_drop_columns = [
    'registered_subject_id',
]

df_apply_functions = {
    'smaller_meals': lambda row: DWTA if row['smaller_meals'] == 'Don\'t want to answer' else row['smaller_meals'],
    'flooring_type': lambda row: DWTA if row['flooring_type'] == 'Don\'t want to answer' else row['flooring_type'],
    'water_source': lambda row: DWTA if row['water_source'] == 'Don\'t want to answer' else row['water_source'],
    'energy_source': lambda row: DWTA if row['energy_source'] == 'Don\'t want to answer' else row['energy_source'],
    'toilet_facility': lambda row: DWTA if row['toilet_facility'] == 'Don\'t want to answer' else row['toilet_facility'],
}


site_recipes.register(ModelRecipe(
    model_name='member.householdinfo',
    old_model_name='bcpp_household_member.householdinfo',
    df_drop_columns=['registered_subject_id', 'household_member_id'],
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
