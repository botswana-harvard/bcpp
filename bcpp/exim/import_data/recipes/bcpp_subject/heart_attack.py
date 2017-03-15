from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
# from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    # 'grant_type': lambda row: common_choices(row['grant_type']),
}

m2m_recipes = [
    M2mRecipe(
        field_name='dx_heart_attack',
        data_model_name='bcpp_subject.heartattack',
        old_data_model_app_label='bcpp_subject',
        list_model_name='bcpp_subject.heartdisease',
        old_list_model_name='bcpp_list.heartdisease',
        join_lists_on='name'),
]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.heartattack',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
