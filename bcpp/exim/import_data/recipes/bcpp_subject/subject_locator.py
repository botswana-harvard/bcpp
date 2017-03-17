import numpy as np
import pandas as pd

from edc_constants.constants import NO
# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

"""
Because registered_subject and subject_visit have been removed, subjct_identifier
must be updated before import.

Use an OUTFILE with recipe.export_raw_df.
"""


def telephone(value):
    if pd.isnull(value):
        return value
    else:
        try:
            return str(int(value))
        except ValueError:
            return str(int(value.replace('-', '')))
    return value


def textfield(value, length=None):
    if pd.isnull(value):
        return np.NaN
    value.replace('  ', ' ').replace('\r\r', '\r')
    if len(value) > length:
        return value[:length]
    return value

df_drop_columns = [
    'exported_datetime', 'export_change_type', 'exported', 'export_uuid',
    'subject_visit_id', 'date_signed']

df_add_columns = []

df_rename_columns = {
    'registered_subject_id': 'subject_identifier'}

df_apply_functions = {
    'has_alt_contact': lambda row: common_choices(row['has_alt_contact'], na=NO),
    'home_visit_permission': lambda row: common_choices(row['home_visit_permission'], na=NO),
    'may_follow_up': lambda row: common_choices(row['may_follow_up'], na=NO),
    'may_sms_follow_up': lambda row: common_choices(row['may_sms_follow_up'], na=NO),
    'may_call_work': lambda row: common_choices(row['may_call_work'], na=NO),
    'may_contact_someone': lambda row: common_choices(row['may_contact_someone'], na=NO),
    'alt_contact_cell': lambda row: telephone(row['alt_contact_cell']),
    'contact_phone': lambda row: telephone(row['contact_phone']),
    'subject_cell': lambda row: telephone(row['subject_cell']),
    'subject_cell_alt': lambda row: telephone(row['subject_cell_alt']),
    'subject_phone': lambda row: telephone(row['subject_phone']),
    'subject_phone_alt': lambda row: telephone(row['subject_phone_alt']),
    'subject_work_phone': lambda row: telephone(row['subject_work_phone']),
    'contact_cell': lambda row: telephone(row['contact_cell']),
    'alt_contact_tel': lambda row: telephone(row['alt_contact_tel']),
    'other_alt_contact_cell': lambda row: telephone(row['other_alt_contact_cell']),
    'alt_contact_cell_number': lambda row: telephone(row['alt_contact_cell_number']),
    'subject_identifier': lambda row: row['subject_identifier'].replace('-', ''),
    'physical_address': lambda row: textfield(row['physical_address'], length=500),
    'contact_physical_address': lambda row: textfield(row['contact_physical_address'], length=500),
    'mail_address': lambda row: textfield(row['mail_address'], length=500),
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
