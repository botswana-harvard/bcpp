# from ...m2m_recipe import M2mRecipe
from bcpp_subject.models import Education
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {}

# for field in Education._meta.get_fields():
#     try:
#         if field.choices:
#             df_apply_functions.update({
#                 field.name: lambda row: common_choices(row[field.name])})
#     except AttributeError:
#         pass


m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.education',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
