# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'household_income': lambda row: common_choices(row['household_income']),
    'monthly_income': lambda row: common_choices(row['monthly_income']),
    'salary_payment': lambda row: common_choices(row['salary_payment']),
    'govt_grant': lambda row: common_choices(row['govt_grant']),
    'employed': lambda row: common_choices(row['employed']),
    'other_occupation': lambda row: common_choices(row['other_occupation']),
    'weeks_out': lambda row: common_choices(row['weeks_out']),
    'occupation': lambda row: common_choices(row['occupation']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.labourmarketwages',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
