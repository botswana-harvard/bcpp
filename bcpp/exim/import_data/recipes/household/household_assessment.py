from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ..bcpp_subject.common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'potential_eligibles': lambda row: common_choices(row['potential_eligibles']),
    'eligibles_last_seen_home': lambda row: common_choices(row['eligibles_last_seen_home']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='household.householdassessment',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
