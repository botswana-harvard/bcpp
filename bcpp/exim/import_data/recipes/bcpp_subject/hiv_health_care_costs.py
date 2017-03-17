# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from edc_constants.constants import NOT_APPLICABLE

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'hiv_medical_care': lambda row: common_choices(row['hiv_medical_care']),
    'reason_no_care': lambda row: common_choices(row['reason_no_care']),
    'place_care_received': lambda row: common_choices(row['place_care_received'], na=NOT_APPLICABLE),
    'care_regularity': lambda row: common_choices(row['care_regularity']),
    'doctor_visits': lambda row: common_choices(row['doctor_visits']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivhealthcarecosts',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
