from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'vote_engagement': lambda row: common_choices(row['vote_engagement']),
    'solve_engagement': lambda row: common_choices(row['solve_engagement']),
    'community_engagement': lambda row: common_choices(row['community_engagement']),
}


m2m_recipes = [
    M2mRecipe(
        field_name='problems_engagement',
        data_model_name='bcpp_subject.communityengagement',
        old_data_model_app_label='bcpp_subject',
        list_model_name='bcpp_subject.neighbourhoodproblems',
        old_list_model_name='bcpp_list.neighbourhoodproblems',
        join_lists_on='name'),
]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.communityengagement',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
