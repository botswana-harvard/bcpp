from datetime import datetime
from dateutil.relativedelta import relativedelta

from .split_weekdays import split_weekdays


def next_clinic_date(community_clinic_days, base_datetime=None, allow_same_day=None, subtract=None):
    """Returns next clinic date that is not today or None.

    community_clinic_days format is a ClinicDaysTuple. See bcpp_household.mappers for format.

    """
    clinic_dates = []
    next_clinic_datetime = None
    if community_clinic_days:
        base_datetime = base_datetime or datetime.today()
        for DAY in community_clinic_days.days:
            if allow_same_day:
                clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
            elif base_datetime + relativedelta(weekday=DAY(+1)) != base_datetime:
                clinic_dates.append(base_datetime + relativedelta(weekday=DAY(+1)))
        if not clinic_dates:
            clinic_dates.append(base_datetime + relativedelta(days=1, weekday=DAY(+1)))
        next_clinic_datetime = datetime(
            min(clinic_dates).year, min(clinic_dates).month, min(clinic_dates).day, 7, 30, 0)
        if subtract and next_clinic_datetime != base_datetime:
            # work back to a clinic day, e.g the nearest clinic day within two weeks
            days = list(community_clinic_days.days)
            days = split_weekdays(days, base_datetime)
            base_datetime = datetime(base_datetime.year, base_datetime.month, base_datetime.day, 7, 30, 0)
            next_clinic_datetime = base_datetime
            for DAY in days:
                next_clinic_datetime = next_clinic_datetime + relativedelta(weekday=DAY(-1))
                if allow_same_day and next_clinic_datetime == base_datetime:
                    break
                elif next_clinic_datetime < base_datetime:
                    break
#         if not (datetime.today() < next_clinic_datetime < last_referal_date):
#             raise CLinicReferalDateError(
#                 "The next clinic date: {0} is not within 7 days. Participant to be referred within 7 days.".format(next_clinic_datetime))
    return next_clinic_datetime
