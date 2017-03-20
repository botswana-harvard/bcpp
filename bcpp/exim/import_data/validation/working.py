import pandas as pd
import numpy as np
from edc_constants.constants import NEG, POS, NAIVE, NO, YES
from bcpp_subject.subject_helper.constants import DEFAULTER, ON_ART

dfe = pd.read_csv('/Users/erikvw/bcpp_201703/kb_20170317.csv', low_memory=True)
dfk = pd.read_csv(
    '/Users/erikvw/Downloads/most_recent_expanded_16mar17.csv', low_memory=True)
df = pd.merge(
    dfe, dfk, on='subject_identifier', how='left', suffixes=['', '_k'])
hiv = {1.0: POS, 0.0: NEG}
df['final_hiv_status_k'] = df['final_hiv_status_k'].map(hiv.get)

arv = {1.0: NAIVE, 2.0: DEFAULTER, 3.0: ON_ART}
df['final_arv_status_k'] = df.apply(lambda row: np.NaN if pd.isnull(
    row['final_arv_status_k']) else row['final_arv_status_k'], axis=1)
df['final_arv_status_k'] = df['final_arv_status_k'].map(arv.get)


# final_hiv_status
df1 = df[(pd.notnull(df['final_hiv_status']) & pd.notnull(df['final_hiv_status_k'])) & (df['final_hiv_status'] != df['final_hiv_status_k'])][
    ['subject_identifier', 'final_hiv_status', 'final_hiv_status_k']]

# final_arv_status
df2 = df[df['final_arv_status'] != df['final_arv_status_k']][
    ['subject_identifier', 'final_arv_status', 'final_arv_status_k']]

# prev_result
df3 = df[df['prev_result'] != df['prev_result_k']][
    ['subject_identifier', 'prev_result', 'prev_result_k']]


# prev_result_known
def prev_result_known(value):
    try:
        return YES if int(value.bool()) == 1 else NO
    except ValueError:
        pass
    return value

df['prev_result_known'] = df.apply(
    lambda row: prev_result_known(df['prev_result_known']), axis=1)

df['prev_result_known_k'] = df['prev_result_known_k'].map(prev2.get)

df4 = df[df['prev_result_known'] is True & df['prev_result_known_k'] is False][
    ['subject_identifier', 'prev_result_known', 'prev_result_known_k']]
