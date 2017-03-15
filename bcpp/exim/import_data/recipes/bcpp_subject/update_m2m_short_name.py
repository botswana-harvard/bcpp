from edc_constants.constants import OTHER, DWTA


def update_m2m_short_name(value):
    if value == 'Other':
        return OTHER
    elif value == 'Don\'t want to answer':
        return DWTA
    return value
