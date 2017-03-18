from bcpp_subject.models import SubjectConsent, Enrollment

qs = SubjectConsent.objects.all().order_by('consent_datetime')
total = qs.count()


sql = (
    'INSERT INTO bcpp_subject_enrollment (report_datetime,is_eligible,id,facility_name,subject_identifier,household_member_id, survey_schedule, survey,visit_schedule_name, schedule_name, created, modified,user_created, user_modified,hostname_created, hostname_modified, revision,consent_identifier) '
    'SELECT C.consent_datetime as report_datetime, True as is_eligible,replace(uuid(),\'-\',\'\') as id, '
    'SUBSTRING(APPT.survey,29,100)  as facility_name, '
    'APPT.subject_identifier, APPT.household_member_id, APPT.survey_schedule, APPT.survey, '
    'APPT.visit_schedule_name, APPT.schedule_name, APPT.created, APPT.modified, '
    'APPT.user_created, APPT.user_modified, '
    'APPT.hostname_created, APPT.hostname_modified, APPT.revision, '
    'REPLACE(C.consent_identifier,\'-\',\'\') as consent_identifier '
    'FROM bcpp_subject_appointment as APPT '
    'LEFT JOIN bcpp_subject_subjectconsent as C '
    'ON (APPT.household_member_id=C.household_member_id) '
    'WHERE C.consent_identifier IS NOT NULL '
    'GROUP BY APPT.subject_identifier,APPT.visit_schedule_name,APPT.schedule_name;')


class Enroll:

    def __init__(self):
        self.enrollments = []
        qs = SubjectConsent.objects.all().order_by('consent_datetime')
        total = qs.count()
        for i in range(0, total):
            print(i)
            print(qs[i])
            self.enroll(qs[i])

    def enroll(self, instance):
        self.enrollments.append(Enrollment.objects.enroll_to_next_survey(
            subject_identifier=instance.subject_identifier,
            household_member=instance.household_member,
            consent_identifier=instance.consent_identifier,
            report_datetime=instance.report_datetime, save=False))
