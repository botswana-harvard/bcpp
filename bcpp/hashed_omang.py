import hashlib
from bcpp_subject.models import SubjectConsent

f = open('/home/django/source/pos_participants_forPIMS_18JUL18.csv', 'r')
lines = f.readlines()
heading = lines[0]
heading = heading.strip()
heading = heading.split(',')
lines.pop(0)
data = []
heading.append('identity256')
data.append(heading)

for line in lines:
    line = line.strip()
    line = line.split(',')
    if len(line) == 4:
        subject_consent = SubjectConsent.objects.filter(subject_identifier=line[2])
        if not subject_consent:
            print(f'There is a pproblem missing subject consent: {line[2]}')
        else:
            identity = subject_consent[0].identity
            identity256 = hashlib.sha256(identity.encode()).hexdigest()
            line.append(identity256)
            data.append(line)
    else:
        print('something wrong with the data')


import csv

with open('/home/django/pos_participants_forPIMS_18JUL18_with_identity256.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerows(data)
