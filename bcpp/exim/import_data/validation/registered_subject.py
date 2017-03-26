from edc_registration.models import RegisteredSubject

from member.models import HouseholdMember

# in HHM not in RS
qs = RegisteredSubject.objects.values('registration_identifier').all()
registration_identifiers = [obj.get('registration_identifier') for obj in qs]
members = HouseholdMember.objects.exclude(
    internal_identifier__in=registration_identifiers)
members.count()  # 1

# in RS not in HHM
qs = HouseholdMember.objects.values('internal_identifier').all()
hhms = [obj.get('internal_identifier') for obj in qs]
hhms = list(set(hhms))
hhms = [x.hex for x in hhms]

rs = RegisteredSubject.objects.exclude(registration_identifier__in=hhms)
subject_identifiers = [obj.subject_identifier for obj in rs]
subject_identifiers = list(set(subject_identifiers))
subject_identifiers = list(set(subject_identifiers))
len(subject_identifiers)  # 159
