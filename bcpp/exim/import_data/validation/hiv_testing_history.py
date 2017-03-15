import pandas as pd

from django.db import connection

sql = (
    'SELECT has_tested, subject_identifier, v.report_datetime '
    'FROM bcpp_subject_hivtestinghistory as A '
    'LEFT JOIN bcpp_subject_subjectvisit as on A.subject_visit_id=V.id')

with connection.cursor() as cursor:
    cursor.execute(sql)
    rows = cursor.fetchall()

fields = ['has_tested', 'subject_identifier', 'report_datetime']
data = {}
for index, field in enumerate(fields):
    data.update({field: [row[index] for row in rows]})

df = pd.DataFrame(data)
df.to_csv('/Users/erikvw/bcpp_201703/kw_hivtestinghistory.csv',
          index=False, encoding='utf-8')
