from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU


def split_seq(seq, sep):
    start = 0
    while start < len(seq):
        try:
            stop = start + seq[start:].index(sep)
            yield seq[start:stop]
            start = stop + 1
        except ValueError:
            yield seq[start:]
            break


def split_weekdays(days, base_datetime):
    """Returns a list of day objects in reversed order.

    For example: given a start day of WED the reverse of
    [MO, TH FR] is [MO, FR TH] in that from WED the previous
    day is MO, then FRI, then TH working backwards.
    """
    wk = [MO, TU, WE, TH, FR, SA, SU]
    weekdays = [day.weekday for day in days]
    weekdays.append(base_datetime.weekday())
    weekdays.sort()
    reversed_days = []
    for item in [x for x in split_seq(weekdays, base_datetime.weekday())]:
        item.reverse()
        for i in item:
            reversed_days.append(i)
    return [wk[i] for i in reversed_days]
