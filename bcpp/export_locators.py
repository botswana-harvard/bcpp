from attr._compat import TYPE
f = open('/home/django/locator.csv', 'r')
lines =  f.readlines()
lines.pop(0)
lines.pop(0)
data = []

for line in lines:
    line = line.strip()
    line = line.split(',')
    data.append(line)

identifiers = []

for d in data:
    identifiers.append(d[1])

locators = SubjectLocator.objects.filter(subject_visit__subject_identifier__in=identifiers)
locator_data = []
fields_list = ['created',
 'modified',
 'user_created',
 'user_modified',
 'hostname_created',
 'hostname_modified',
 'revision',
 'id',
 'consent_version',
 'report_datetime',
 'mail_address',
 'home_visit_permission',
 'physical_address',
 'may_follow_up',
 'may_sms_follow_up',
 'subject_cell',
 'subject_cell_alt',
 'subject_phone',
 'subject_phone_alt',
 'may_call_work',
 'subject_work_place',
 'subject_work_phone',
 'may_contact_someone',
 'contact_name',
 'contact_rel',
 'contact_physical_address',
 'contact_cell',
 'contact_phone',
 'alt_contact_cell_number',
 'has_alt_contact',
 'alt_contact_name',
 'alt_contact_rel',
 'alt_contact_cell',
 'other_alt_contact_cell',
 'alt_contact_tel']

for l in locators:
    d = {}
    for f in fields_list:
        d[f] = getattr(l, f)
    d.update(subject_identifier=l.subject_visit.subject_identifier)
    locator_data.append(d)

from django.core.serializers.json import DjangoJSONEncoder
import json
with open('l_data.json', 'w') as outfile:
    json.dump(locator_data, outfile, cls=DjangoJSONEncoder)
    
    

with open('/home/django/source/l_data.json') as f:
    data = json.load(f)

date_fields = ['created', 'modified', 'report_datetime', ]
from dateutil import parser
    
for d in data:
    try:
        created = parser.parse(d.get('created'))
        d.update(created=created)
    except TypeError:
        pass
    try:
        modified = parser.parse(d.get('modified'))
        d.update(modified=modified, )
    except TypeError:
        pass
    try:
        report_datetime = parser.parse(d.get('report_datetime'))
        d.update(report_datetime=report_datetime)
    except TypeError:
        pass
    try:
        SubjectLocator.objects.get(subject_identifier=d.get('subject_identifier'))
    except SubjectLocator.DoesNotExist:
        locator = SubjectLocator(**d)
        locator.save_base()
    






created = parser.parse(l.get('created'))
modified = parser.parse(l.get('modified'))
report_datetime = parser.parse(l.get('report_datetime'))