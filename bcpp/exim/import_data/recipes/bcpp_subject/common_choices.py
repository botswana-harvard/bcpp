import pandas as pd
import numpy as np

from edc_constants.constants import (
    UNKNOWN, OTHER, DWTA, NOT_SURE, NEG, POS,
    NOT_APPLICABLE, REFUSED)

from bcpp_subject.constants import DAYS, YEARS, MONTHS


def common_choices(value, na=None):
    na = na or np.NaN
    if pd.isnull(value):
        return na
    elif value.lower() == 'other':
        return OTHER
    elif value == 'not_answering':
        return DWTA
    elif value == 'Don\'t want to answer':
        return DWTA
    elif value == 'UNK':
        return UNKNOWN
    elif value in ['Not Sure', 'I am not sure', 'Not sure']:
        return NOT_SURE
    elif value == 'Not applicable':
        return NOT_APPLICABLE
    elif value == 'Refuse':
        return REFUSED
    elif value == 'Days':
        return DAYS
    elif value == 'Years':
        return YEARS
    elif value == 'Months':
        return MONTHS
    elif value == 'negative':
        return NEG
    elif value == 'positive':
        return POS
    elif value == 'None':
        return na
    return value
