import uuid

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ..bcpp_subject.common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'transaction': lambda row: uuid.UUID(row['transaction']).hex,
    'reason': lambda row: common_choices(row['reason']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='household.householdrefusalhistory',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
