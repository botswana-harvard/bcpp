import pandas as pd
from ...recipe import site_recipes


def import_duplicate_members():
    """Returns a recipe.

    Imports excluded household members, originally flagged as duplicates,
    who have consented.

    """

    #     sql = (
    #         "SELECT a.household_member_id AS household_member_id "
    #         "FROM bhp066.bcpp_subject_subjectconsent AS a "
    #         "LEFT JOIN member_householdmember AS b "
    #         "ON replace(a.household_member_id, '-', '') = b.id "
    #         "WHERE b.id is NULL;")
    df_old_members = pd.read_csv(
        '/Users/erikvw/bcpp_201703/bcpp_household_member/householdmember.csv',
        low_memory=False,
        encoding='utf-8',
        sep='|',
        lineterminator='\n',
        escapechar='\\')
    df_members = pd.read_csv(
        '/Users/erikvw/bcpp_201703/new/member/householdmember.csv',
        low_memory=False,
        encoding='utf-8',
        sep='|',
        lineterminator='\n',
        escapechar='\\')
    df_consents = pd.read_csv(
        '/Users/erikvw/bcpp_201703/new/bcpp_subject/subjectconsent4mysql.csv',
        low_memory=False,
        encoding='utf-8',
        sep='|',
        lineterminator='\n',
        escapechar='\\')
    df = pd.merge(df_consents, df_members, left_on='household_member_id',
                  right_on='id', how='left', suffixes=('', '_y'))
    df_missing = df_old_members[
        df_old_members['id'].isin(df[df['id_y'].isnull()]['household_member_id'])]
    df_missing.to_csv(
        path_or_buf='/Users/erikvw/bcpp_201703/new/member/householdmember.consented.dups.csv',
        index=False,
        encoding='utf-8',
        sep='|',
        lineterminator='\n',
        escapechar='\\')
    recipe = site_recipes.recipes.get('member.householdmember')
    recipe.in_path = '/Users/erikvw/bcpp_201703/new/member/householdmember.consented.dups.csv'
    recipe.df_apply_functions.update({
        'initials': lambda row: '{}Z{}'.format(row['initials'][0], row['initials'][1])})
    recipe.import_csv()
    return recipe
