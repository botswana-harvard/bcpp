from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .recent_partner import update_m2m_options, df_apply_functions


df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = df_apply_functions


m2m_recipes = [
    M2mRecipe(
        field_name='first_partner_live',
        data_model_name='bcpp_subject.thirdpartner',
        old_data_model_app_label='bcpp_subject',
        old_data_model_model_name='monthsthirdpartner',
        list_model_name='bcpp_subject.partnerresidency',
        old_list_model_name='bcpp_list.partnerresidency',
        join_lists_on='short_name',
        df_apply_functions={
            'short_name': lambda row: update_m2m_options(row['short_name'])}
    )
]


site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.thirdpartner',
    old_model_name='bcpp_subject.monthsthirdpartner',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
