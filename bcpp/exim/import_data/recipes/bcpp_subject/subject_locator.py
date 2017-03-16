# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = [
    'exported_datetime', 'export_change_type', 'exported', 'export_uuid']

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'has_alt_contact': lambda row: common_choices(row['has_alt_contact']),
    'home_visit_permission': lambda row: common_choices(row['home_visit_permission']),
    'may_follow_up': lambda row: common_choices(row['may_follow_up']),
    'may_sms_follow_up': lambda row: common_choices(row['may_sms_follow_up']),
    'may_call_work': lambda row: common_choices(row['may_call_work']),
    'may_contact_someone': lambda row: common_choices(row['may_contact_someone']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.subjectlocator',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
