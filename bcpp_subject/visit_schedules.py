import sys
from django.core.management.color import color_style

from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.visit_schedule import VisitSchedule
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Crf
from edc_map.site_mappers import site_mappers

style = color_style()

crfs_baseline = (
    Crf(show_order=10, model='bcpp_subject.subjectlocator', required=True),
    Crf(show_order=20, model='bcpp_subject.residencymobility', required=True),
    Crf(show_order=30, model='bcpp_subject.communityengagement', required=True),
    Crf(show_order=40, model='bcpp_subject.demographics', required=True),
    Crf(show_order=50, model='bcpp_subject.education', required=True),
    Crf(show_order=60, model='bcpp_subject.hivtestinghistory', required=True),
    Crf(show_order=70, model='bcpp_subject.hivtestreview', required=True),
    Crf(show_order=80, model='bcpp_subject.hivresultdocumentation', required=True),
    Crf(show_order=90, model='bcpp_subject.hivtested', required=True),
    Crf(show_order=100, model='bcpp_subject.hivuntested', required=True),
    Crf(show_order=120, model='bcpp_subject.sexualbehaviour', required=True),
    Crf(show_order=130, model='bcpp_subject.monthsrecentpartner', required=True),
    Crf(show_order=140, model='bcpp_subject.monthssecondpartner', required=True),
    Crf(show_order=150, model='bcpp_subject.monthsthirdpartner', required=True),
    Crf(show_order=160, model='bcpp_subject.hivcareadherence', required=True),
    Crf(show_order=170, model='bcpp_subject.hivmedicalcare', required=True),
    Crf(show_order=180, model='bcpp_subject.circumcision', required=True),
    Crf(show_order=190, model='bcpp_subject.circumcised', required=True),
    Crf(show_order=200, model='bcpp_subject.uncircumcised', required=True),
    Crf(show_order=210, model='bcpp_subject.reproductivehealth', required=True),
    Crf(show_order=220, model='bcpp_subject.pregnancy', required=True),
    Crf(show_order=230, model='bcpp_subject.nonpregnancy', required=True),
    Crf(show_order=240, model='bcpp_subject.medicaldiagnoses', required=True),
    Crf(show_order=250, model='bcpp_subject.heartattack', required=True),
    Crf(show_order=260, model='bcpp_subject.cancer', required=True),
    Crf(show_order=270, model='bcpp_subject.sti', required=True),
    Crf(show_order=280, model='bcpp_subject.tubercolosis', required=True),
    Crf(show_order=290, model='bcpp_subject.tbsymptoms', required=True),
    Crf(show_order=300, model='bcpp_subject.substanceuse', required=True),
    Crf(show_order=320, model='bcpp_subject.stigma', required=True),
    Crf(show_order=330, model='bcpp_subject.stigmaopinion', required=True),
    Crf(show_order=340, model='bcpp_subject.positiveparticipant', required=True),
    Crf(show_order=350, model='bcpp_subject.accesstocare', required=True),
    Crf(show_order=360, model='bcpp_subject.hivlinkagetocare', required=True),
    Crf(show_order=370, model='bcpp_subject.hivresult', required=True),
    Crf(show_order=380, model='bcpp_subject.elisahivresult', required=False, additional=True),
    Crf(show_order=390, model='bcpp_subject.pima', required=False, additional=True),
    Crf(show_order=400, model='bcpp_subject.subjectreferral', required=True),
    Crf(show_order=410, model='bcpp_subject.hicenrollment', required=False, additional=True),
)

crfs_annual = (
    Crf(show_order=10, model='bcpp_subject.residencymobility', required=True),
    Crf(show_order=20, model='bcpp_subject.demographics', required=True),
    Crf(show_order=30, model='bcpp_subject.education', required=True),
    Crf(show_order=40, model='bcpp_subject.hivtestinghistory', required=True),
    Crf(show_order=50, model='bcpp_subject.hivtestreview', required=True),
    Crf(show_order=60, model='bcpp_subject.hivresultdocumentation', required=True),
    Crf(show_order=70, model='bcpp_subject.hivtested', required=True),
    Crf(show_order=80, model='bcpp_subject.hivuntested', NOT_required=True),
    Crf(show_order=90, model='bcpp_subject.sexualbehaviour', required=True),
    Crf(show_order=100, model='bcpp_subject.monthsrecentpartner', required=True),
    Crf(show_order=110, model='bcpp_subject.monthssecondpartner', required=True),
    Crf(show_order=120, model='bcpp_subject.monthsthirdpartner', required=True),
    Crf(show_order=130, model='bcpp_subject.hivcareadherence', required=True),
    Crf(show_order=140, model='bcpp_subject.hivmedicalcare', required=True),
    Crf(show_order=150, model='bcpp_subject.circumcision', required=True),
    Crf(show_order=160, model='bcpp_subject.circumcised', required=True),
    Crf(show_order=170, model='bcpp_subject.uncircumcised', required=True),
    Crf(show_order=180, model='bcpp_subject.reproductivehealth', required=True),
    Crf(show_order=190, model='bcpp_subject.pregnancy', required=True),
    Crf(show_order=200, model='bcpp_subject.nonpregnancy', required=True),
    Crf(show_order=210, model='bcpp_subject.medicaldiagnoses', required=True),
    Crf(show_order=220, model='bcpp_subject.heartattack', required=True),
    Crf(show_order=230, model='bcpp_subject.cancer', required=True),
    Crf(show_order=240, model='bcpp_subject.sti', required=True),
    Crf(show_order=250, model='bcpp_subject.tubercolosis', required=True),
    Crf(show_order=260, model='bcpp_subject.tbsymptoms', required=True),
    Crf(show_order=270, model='bcpp_subject.qualityoflife', required=True),
    Crf(show_order=280, model='bcpp_subject.resourceutilization', required=True),
    Crf(show_order=290, model='bcpp_subject.outpatientcare', required=True),
    Crf(show_order=300, model='bcpp_subject.hospitaladmission', required=True),
    Crf(show_order=310, model='bcpp_subject.hivhealthcarecosts', required=True),
    Crf(show_order=320, model='bcpp_subject.labourmarketwages', required=True),
    Crf(show_order=330, model='bcpp_subject.hivlinkagetocare', required=True),
    Crf(show_order=340, model='bcpp_subject.hivresult', required=True),
    Crf(show_order=350, model='bcpp_subject.elisahivresult', required=False, additional=True),
    Crf(show_order=360, model='bcpp_subject.pima', required=False, additional=True),
    Crf(show_order=370, model='bcpp_subject.subjectreferral', required=True),
    Crf(show_order=380, model='bcpp_subject.hicenrollment', required=False, additional=True),
)

crfs_ess = ()

requisitions = ()

visit_schedule = VisitSchedule(
    name='visit_schedule',
    verbose_name='BCPP Visit Schedule',
    app_label='bcpp_subject',
    visit_model='bcpp_subject.subjectvisit',
)

try:
    if site_mappers.current_mapper.intervention:
        crfs_annual = [crf for crf in crfs_annual
                       if crf.model not in ['bcpp_subject.hivuntested']]
    else:
        crfs_annual = [crf for crf in crfs_annual
                       if crf.model not in ['bcpp_subject.tbsymptoms', 'bcpp_subject.hivuntested']]
except AttributeError:
    sys.stdout.write(style.WARNING(
        '  * WARNING: visit schedule requires the current mapper but the mapper is not set.\n'))

schedule = Schedule(name='survey_schedule', enrollment_model='bcpp_subject.enrollment')

schedule.add_visit(
    code='T0',
    title='Baseline Household Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_baseline)

schedule.add_visit(
    code='T1',
    title='Annual Household Survey',
    timepoint=1,
    base_interval=1,
    requisitions=requisitions,
    crfs=crfs_annual)

schedule.add_visit(
    code='T2',
    title='Annual Household Survey',
    timepoint=2,
    base_interval=2,
    requisitions=requisitions,
    crfs=crfs_annual)

schedule.add_visit(
    code='T3',
    title='End of Study Household Survey',
    timepoint=3,
    base_interval=3,
    requisitions=requisitions,
    crfs=crfs_ess)

visit_schedule.add_schedule(schedule)

site_visit_schedules.register(visit_schedule)
