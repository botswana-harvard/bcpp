from edc_registration.models import RegisteredSubject
from edc_registration.exceptions import RegisteredSubjectError

"""
After loading with mysql LOAD DATA INFILE, resave objects to encrypt.
"""

for obj in RegisteredSubject.objects.all():
    try:
        obj.save()
    except RegisteredSubjectError as e:
        print(str(e))
