# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

# export sql
# import pandas as pd
# from bcpp_export.dataframes.edc.edc_model_to_dataframe import EdcModelToDataFrame
# from bhp066.apps.bcpp_subject.models import Grant, LabourMarketWages
#
# l = EdcModelToDataFrame(model=LabourMarketWages)
# g = EdcModelToDataFrame(model=Grant)
# df = pd.merge(g.dataframe, l.dataframe, left_on='labour_market_wages_id',
#               right_on='id', how='left', suffixes=['', '_lmw'])
# cols = list(g.dataframe.columns)
# cols.sort()
# cols.append('subject_visit_id')
# df.to_csv(columns=cols, path_or_buf='/Users/erikvw/bcpp_201703/bcpp_subject/grant.csv',
#           index=False, encoding='utf-8', sep='|')


df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'grant_type': lambda row: common_choices(row['grant_type']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.grant',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
