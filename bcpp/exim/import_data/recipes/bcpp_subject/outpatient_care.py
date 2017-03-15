# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'govt_health_care': lambda row: common_choices(row['govt_health_care']),
    'dept_care': lambda row: common_choices(row['dept_care']),
    'prvt_care': lambda row: common_choices(row['prvt_care']),
    'trad_care': lambda row: common_choices(row['trad_care']),
    'facility_visited': lambda row: common_choices(row['facility_visited']),
    'care_reason': lambda row: common_choices(row['care_reason']),
    'travel_time': lambda row: common_choices(row['travel_time']),
    'cost_cover': lambda row: common_choices(row['cost_cover']),
    'waiting_hours': lambda row: common_choices(row['waiting_hours']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.outpatientcare',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
