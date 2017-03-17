from ...exceptions import ImportDataError
from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices as base_common_choices
from .update_m2m_short_name import update_m2m_short_name as base_update_m2m_short_name


def common_choices(value):
    value = base_common_choices(value)
    if value == 'Tati Siding':
        return 'Tati_Siding'
    elif value == 'Mandunyane':
        return 'Mmandunyane'
    elif value == 'Raikops':
        return 'Rakops'
    elif value == 'Sefare':
        return 'Sefhare'
    return value


def first_exchange(value):
    value = base_common_choices(value)
    try:
        if 0 <= int(value) <= 18:
            return 'less or equal to 18 years old'
        elif 19 <= int(value) <= 29:
            return '19-29'
        elif 30 <= int(value) <= 39:
            return '30-39'
        elif 40 <= int(value) <= 49:
            return '40-49'
        elif 50 <= int(value) <= 59:
            return '50-59'
        elif 60 <= int(value):
            return '60 or older'
        else:
            raise ImportDataError('Invalid AGE. Got {}'.format(int(value)))
    except ValueError:
        pass
    return value


df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'sex_partner_community': lambda row: common_choices(row['sex_partner_community']),
    'past_year_sex_freq': lambda row: common_choices(row['past_year_sex_freq']),
    'third_last_sex': lambda row: common_choices(row['third_last_sex']),
    'first_first_sex': lambda row: common_choices(row['first_first_sex']),
    'first_sex_current': lambda row: common_choices(row['first_sex_current']),
    'first_relationship': lambda row: common_choices(row['first_relationship']),
    'first_exchange': lambda row: first_exchange(row['first_exchange']),
    'concurrent': lambda row: common_choices(row['concurrent']),
    'goods_exchange': lambda row: common_choices(row['goods_exchange']),
    'first_partner_hiv': lambda row: common_choices(row['first_partner_hiv']),
    'partner_hiv_test': lambda row: common_choices(row['partner_hiv_test']),
    'first_haart': lambda row: common_choices(row['first_haart']),
    'first_disclose': lambda row: common_choices(row['first_disclose']),
    'first_condom_freq': lambda row: common_choices(row['first_condom_freq']),
    'first_partner_cp': lambda row: common_choices(row['first_partner_cp']),
}


def update_m2m_options(value):
    value = base_update_m2m_short_name(value)
    if value == 'in this community':
        return 'inside_community'
    elif value == 'outside community':
        return 'outside_community'
    elif value == 'farm within':
        return 'farm_inside_community'
    elif value == 'farm outside this community':
        return 'farm_outside_community'
    elif value == 'cattelepost within':
        return 'cattelepost_inside_community'
    elif value == 'cattlepost outside':
        return 'cattlepost_outside_community'
    return value

m2m_recipes = [
    M2mRecipe(
        field_name='first_partner_live',
        data_model_name='bcpp_subject.recentpartner',
        old_data_model_app_label='bcpp_subject',
        old_data_model_model_name='monthsrecentpartner',
        list_model_name='bcpp_subject.partnerresidency',
        old_list_model_name='bcpp_list.partnerresidency',
        join_lists_on='short_name',
        df_apply_functions={
            'short_name': lambda row: update_m2m_options(row['short_name'])}
    )
]

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.recentpartner',
    old_model_name='bcpp_subject.monthsrecentpartner',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
