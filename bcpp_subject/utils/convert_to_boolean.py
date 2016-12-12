

def convert_to_nullboolean(yes_no_dwta):
    """Converts 'yes' to True, 'no' to False or returns None."""
    if str(yes_no_dwta) in ['True', 'False', 'None']:
        return yes_no_dwta
    if yes_no_dwta.lower() == 'no':
        return False
    elif yes_no_dwta.lower() == 'yes':
        return True
    else:
        return None
