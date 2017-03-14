from edc_constants.constants import UNKNOWN, OTHER, DWTA, NOT_SURE,\
    NOT_APPLICABLE


def common_choices(value):
    if value == 'Other':
        return OTHER
    elif value == 'not_answering':
        return DWTA
    elif value == 'Don\'t want to answer':
        return DWTA
    elif value == 'UNK':
        return UNKNOWN
    elif value == 'Not Sure':
        return NOT_SURE
    elif value == 'Not applicable':
        return NOT_APPLICABLE
    return value
