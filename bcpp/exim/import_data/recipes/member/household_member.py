import numpy as np

from edc_registration.models import RegisteredSubject

from member.models import HouseholdMember

from ...recipe import site_recipes, Recipe


df_drop_columns = [
    'registered_subject_id',
    'hiv_history',
    'reported',
    'member_status',
    'is_consented',
    'updated_after_auto_filled',
]

df_rename_columns = {
    'auto_filled': 'cloned'}

df_apply_functions = {
    'cloned_datetime': lambda row: row['created'] if row['cloned'] else np.NaN,
    'report_datetime': lambda row: row['created'],
    'citizen': lambda row: row['eligible_subject'],
    'relation': lambda row: 'family_friend' if row['relation'].lower() == 'family friend' else row['relation'].lower(),
    'study_resident': lambda row: np.NaN if row['study_resident'] == 'Unknown' else row['study_resident'],
}


def post_import_handler():
    for obj in HouseholdMember.objects.all():
        try:
            rs = RegisteredSubject.objects.get(
                internal_identifier=obj.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            subject_identifier = None
        else:
            subject_identifier = rs.subject_identifier
        obj.survey_schedule = obj.household_structure.survey_schedule
        obj.subject_identifier = subject_identifier
        obj.household_identifier = obj.household_structure.household.household_identifier
        obj.save_base(raw=True)

site_recipes.register(Recipe(
    model_name='member.householdmember',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    # post_import_handler=post_import_handler,
))
