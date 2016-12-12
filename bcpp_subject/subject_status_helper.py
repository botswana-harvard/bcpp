from copy import copy

from datetime import datetime

from django.apps import apps as django_apps

from edc_constants.constants import POS, NEG

from .constants import BASELINE_CODES
from .models import (
    HivResult, Pima, HivTestReview, HivCareAdherence,
    HivTestingHistory, HivResultDocumentation,
    ElisaHivResult)
from .utils import convert_to_nullboolean


class SubjectStatusHelper(object):
    """A helper class to consistently and conveniently return the
    HIV status of a subject.

    These values refer to information longitudinally:
        * hiv_result: always POS after first POS is reported
        * new_pos: False after the first POS is reported
        * rbd_sample_drawn: only needs to be collected once so True after sample collection
        * vl_sample_drawn:  only needs to be collected once so True after sample collection
    """
    # class attribute is accessed by the signal to ensure
    # any modifications are caught in the post_save signal

    BASELINE = 'baseline'
    ANNUAL = 'annual'

    models = {
        BASELINE: {
            'hiv_care_adherence': HivCareAdherence,
            'hiv_result': HivResult,
            'elisa_hiv_result': ElisaHivResult,
            'hiv_result_documentation': HivResultDocumentation,
            'hiv_test_review': HivTestReview,
            'hiv_testing_history': HivTestingHistory,
            'pima': Pima},
        ANNUAL: {
            'hiv_care_adherence': HivCareAdherence,
            'hiv_result': HivResult,
            'elisa_hiv_result': ElisaHivResult,
            'hiv_result_documentation': HivResultDocumentation,
            'hiv_test_review': HivTestReview,
            'hiv_testing_history': HivTestingHistory,
            'pima': Pima},
    }

    def __init__(self, visit_instance=None, use_baseline_visit=False):
        self._defaulter = None
        self._rbd_requisition_instance = None
        self._documented_verbal_hiv_result = None
        self._documented_verbal_hiv_result_date = None
        self._hiv_care_adherence_instance = None
        self._hiv_result = None
        self._hiv_result_datetime = None
        self._hiv_result_documentation_instance = None
        self._hiv_result_instance = None
        self._elisa_result_instance = None
        self._hiv_test_review_instance = None
        self._hiv_testing_history_instance = None
        self._indirect_hiv_documentation = None
        self._last_hiv_result = None
        self._last_hiv_result_date = None
        self._new_pos = None
        self._on_art = None
        self._pima_instance = None
        self._rbd_sample_drawn = None
        self._rbd_requisition_instance = None
        self._recorded_hiv_result = None
        self._recorded_hiv_result_date = None
        self._todays_cd4_result = None
        self._todays_cd4_result_datetime = None
        self._todays_hiv_result = None
        self._todays_hiv_result_datetime = None
        self._elisa_hiv_result = None
        self._elisa_hiv_result_datetime = None
        self._verbal_hiv_result = None
        self._vl_requisition_instance = None
        self._vl_sample_drawn = None
        self._vl_sample_drawn_datetime = None
        self._subject_visit = None
        self.previous_subject_visits = []
        self.use_baseline_visit = use_baseline_visit
        if visit_instance:
            self.subject_visit = visit_instance
        self.models[self.BASELINE].update({
            'subject_requisition': django_apps.get_model('bcpp_lab', 'SubjectRequisition')})
        self.models[self.ANNUAL].update({
            'subject_requisition': django_apps.get_model('bcpp_lab', 'SubjectRequisition')})

    def __repr__(self):
        return 'SubjectStatusHelper({0.subject_visit!r})'.format(self)

    def __str__(self):
        return '({0.subject_visit!r})'.format(self)

    @property
    def timepoint_key(self):
        """Returns a dictionary key of either baseline or annual base in the visit code."""
        if self.subject_visit.appointment.visit_definition.code in BASELINE_CODES:
            return self.BASELINE
        return self.ANNUAL

    @property
    def subject_visit(self):
        """Returns the visit instance."""
        return self._subject_visit

    @subject_visit.setter
    def subject_visit(self, visit_instance):
        """Sets the visit_instance to the given visit_instance
        or the baseline visit instance if using_baseline=True."""
        Appointment = django_apps.get_model('bcpp_subject', 'Appointment')
        SubjectVisit = django_apps.get_model('bcpp_subject', 'SubjectVisit')
        if self._subject_visit:
            # reset every attribute
            self._subject_visit = None
            self.__init__()
        self._subject_visit = visit_instance
        if self.use_baseline_visit:
            try:
                registered_subject = visit_instance.appointment.registered_subject
                baseline_appointment = Appointment.objects.filter(
                    registered_subject=registered_subject, visit_definition__code__in=BASELINE_CODES)[0]
                self._subject_visit = SubjectVisit.objects.get(
                    household_member__registered_subject=visit_instance.appointment.registered_subject,
                    appointment=baseline_appointment)
            except (SubjectVisit.DoesNotExist, IndexError):
                self._subject_visit = None
        else:
            # prepare a queryset of visits previous to visit_instance
            self.previous_subject_visits = SubjectVisit.objects.filter(
                household_member__internal_identifier=visit_instance.household_member.internal_identifier,
                report_datetime__lt=visit_instance.report_datetime).order_by('report_datetime')

    def visit_code(self):
        return self.subject_visit.appointment.visit_definition.code

    def previous_value(self, value_if_pos=None, value_if_not_pos=None, attr_if_pos=None):
        """Returns the value of an attribute from a previous instance if the hiv_result
        of the previous instance is POS using a previous subject_visit. If the attribute
        provided in attr_if_pos does not exist, then it will return the value of
        \'value_if_pos\'. If there is no previous visit, returns the value of \'value_if_not_pos\'."""
        value = value_if_not_pos
        if self.previous_subject_visits:
            current_subject_visit = copy(self.subject_visit)
            previous_subject_visits = copy(self.previous_subject_visits)
            for subject_visit in previous_subject_visits:
                # check for POS result from previous data
                self.subject_visit = subject_visit
                if self.hiv_result == POS:
                    try:
                        value = None
                        for attr in attr_if_pos:
                            value = getattr(value or self, attr)
                            try:
                                value = value()  # call if not property
                            except TypeError:
                                pass
                    except TypeError:  # attr_if_pos is None, not iterable
                        value = value_if_pos
#                     except AttributeError:# 'SubjectStatusHelper' object has no attribute 'date'
#                         value = value_if_pos
                    break  # got one!
            self.subject_visit = current_subject_visit
        return value

    @property
    def hiv_result(self):
        """Returns the hiv status considering today\'s result, elisa hiv result,
        the last documented result and a verbal result OR a positive result from a
        previous survey."""
        if not self._hiv_result:
            self._hiv_result = self.calculated_hiv_result
        return self._hiv_result

    @property
    def calculated_hiv_result(self):
        """Returns the hiv status considering today\'s result, elisa hiv result,
        the last documented result and a verbal result."""
        return (
            (self.elisa_hiv_result or self.todays_hiv_result) or
            (self.last_hiv_result if self.last_hiv_result == POS else None) or
            (self.documented_verbal_hiv_result if self.documented_verbal_hiv_result == POS else None) or
            (self.verbal_hiv_result if (self.verbal_hiv_result == POS and
                                        (self.direct_hiv_pos_documentation or
                                         self.indirect_hiv_documentation)
                                        ) else None
             )
        )

    @property
    def hiv_result_datetime(self):
        """Returns the oldest hiv result datetime if POS, based on last,
        today or elisa most recent if NEG."""
        if not self._hiv_result_datetime:
            last_hiv_result_datetime = None
            if self.last_hiv_result_date:
                # Documented Hiv Result, No test done => POS.
                last_hiv_result_datetime = datetime(self.last_hiv_result_date.year,
                                                    self.last_hiv_result_date.month,
                                                    self.last_hiv_result_date.day)
#                                                     self.last_hiv_result_date.hour,
#                                                     self.last_hiv_result_date.minute,
#                                                     self.last_hiv_result_date.second,
#                                                     self.last_hiv_result_date.millisecond)
            if self.hiv_result == POS:
                # self.hiv_result == POS could be known POS or from Today's Hiv Result
                # of from Elisa's Hiv Result
                if self.last_hiv_result == POS:
                    self._hiv_result_datetime = last_hiv_result_datetime
                else:
                    # else it could be that of normal hiv_result or elisa hiv_result. The two are mutually exclusive.
                    self._hiv_result_datetime = (self.todays_hiv_result_datetime or
                                                 self.elisa_hiv_result_datetime)
            else:
                self._hiv_result_datetime = (self.elisa_hiv_result_datetime or
                                             self.todays_hiv_result_datetime or
                                             last_hiv_result_datetime)  # take latest if not POS
        return self._hiv_result_datetime

    @property
    def new_pos(self):
        """Returns True if combination of documents and test history show POS."""
        if self._new_pos is None:
            previous_pos = None
            previous_pos = self.previous_value(value_if_pos=POS, value_if_not_pos=None)
            if previous_pos:
                # This takes care of previous enrollees, those now doing annual survey.
                new_pos = False
            else:
                new_pos = False
                # You have not been tested today, but you have documentation of a posetive
                # past status.
                if (not (self.todays_hiv_result == POS or self.elisa_hiv_result == POS) and
                        (self.direct_hiv_pos_documentation or self.indirect_hiv_documentation)):
                    pass
                # You only have today's result and possibly an undocumented verbal_hiv_result
                elif ((self.todays_hiv_result == POS or self.elisa_hiv_result == POS) and not
                        (self.direct_hiv_pos_documentation or self.indirect_hiv_documentation)):
                    new_pos = True
                else:
                    # may have no result or just an undocumented verbal_hiv_result,
                    # which is not enough information.
                    new_pos = None
            self._new_pos = new_pos
        return self._new_pos

    @property
    def arv_documentation(self):
        """Returns True is there is arv documentation otherwise False or None."""
        try:
            arv_documentation = convert_to_nullboolean(self.hiv_care_adherence_instance.arv_evidence)
        except AttributeError:
            arv_documentation = None
        return arv_documentation

    @property
    def cd4_result_datetime(self):
        """Returns the datetim of the CD4 result run in the household."""
        return self.todays_cd4_result_datetime

    @property
    def documented_verbal_hiv_result(self):
        """Returns an hiv result based on the confirmation of the verbal result by documentation."""
        if not self._documented_verbal_hiv_result:
            try:
                # self._documented_verbal_hiv_result = self.hiv_result_documentation_instance.result_recorded
                self._documented_verbal_hiv_result = (POS if (self.indirect_hiv_documentation or
                                                              self.direct_hiv_pos_documentation) else None)
            except AttributeError:
                self._documented_verbal_hiv_result = None
        return self._documented_verbal_hiv_result

    @property
    def documented_verbal_hiv_result_date(self):
        """Returns an hiv result based on the confirmation of the verbal result by documentation."""
        if not self._documented_verbal_hiv_result_date:
            try:
                self._documented_verbal_hiv_result_date = (self.hiv_result_documentation_instance.result_date if
                                                           self.hiv_result_documentation_instance else
                                                           self.hiv_care_adherence_instance.first_arv)
            except AttributeError:
                self._documented_verbal_hiv_result_date = None
        return self._documented_verbal_hiv_result_date

    @property
    def cd4_result(self):
        """Returns the value of the CD4 run in the household."""
        return self.todays_cd4_result

    @property
    def defaulter(self):
        """Returns true if subject is an ARV defaulter."""
        if not self._defaulter:
            try:
                if (self.hiv_care_adherence_instance.on_arv == 'No' and
                        self.hiv_care_adherence_instance.arv_evidence == 'Yes'):
                    self._defaulter = True
                elif (self.hiv_care_adherence_instance.on_arv == 'No' and
                        self.hiv_care_adherence_instance.ever_taken_arv == 'Yes'):
                    self._defaulter = True
                else:
                    self._defaulter = False
            except AttributeError:
                self._defaulter = None
        return self._defaulter

    @property
    def direct_hiv_documentation(self):
        """Returns True if documentation of an HIV test was seen."""
        direct_hiv_documentation = self.previous_value(value_if_pos=True, value_if_not_pos=False)
        if not direct_hiv_documentation:
            direct_hiv_documentation = True if self.recorded_hiv_result in [POS, NEG] else False
        return direct_hiv_documentation

    @property
    def direct_hiv_pos_documentation(self):
        """Returns True if documentation of a POS HIV test was seen."""
        return True if (self.recorded_hiv_result == POS) else False

    @property
    def indirect_hiv_documentation(self):
        """Returns True if there is a verbal result and hiv_testing_history.other_record
        is Yes, otherwise None (not False).

        hiv_testing_history.other_record or hiv_care_adherence.arv_evidence is indirect
        evidence of a previous "POS result" only."""
        try:
            if self.verbal_hiv_result == POS:
                if self.hiv_testing_history_instance.other_record == 'Yes' or self.arv_documentation:
                    self._indirect_hiv_documentation = True
                else:
                    self._indirect_hiv_documentation = False
        except AttributeError:
            self._indirect_hiv_documentation = None
        return self._indirect_hiv_documentation

    @property
    def last_hiv_result(self):
        """Returns True the last HIV result which is either the recorded
        result or a verbal result supported by direct or indirect documentation."""
        if not self._last_hiv_result:
            last_hiv_result = None
            last_hiv_result = self.previous_value(value_if_pos=POS, value_if_not_pos=None)
            # If there is no POS from a previous visit instance result, then check the status of this
            # visit instance. It could be that after you tested them, they tested POS later elsewhere
            # and have documentation to prove it.
            if not last_hiv_result:
                last_hiv_result = self.recorded_hiv_result or self.documented_verbal_hiv_result
            self._last_hiv_result = last_hiv_result
        return self._last_hiv_result

    @property
    def last_hiv_result_date(self):
        if not self._last_hiv_result_date:
            last_hiv_result_date = None
            last_hiv_result_date = self.previous_value(
                # attr_if_pos=('hiv_result_datetime', 'date'),
                attr_if_pos=('hiv_result_datetime',),
                value_if_not_pos=None)
            if not last_hiv_result_date:
                last_hiv_result_date = (self.recorded_hiv_result_date or
                                        self.documented_verbal_hiv_result_date)
            self._last_hiv_result_date = last_hiv_result_date
        return self._last_hiv_result_date

    @property
    def on_art(self):
        if self._on_art is None:
            try:
                if self.hiv_care_adherence_instance.on_arv == 'Yes':
                    self._on_art = True
                elif self.defaulter:
                    self._on_art = True
                else:
                    self._on_art = False
            except AttributeError:
                if self.new_pos:
                    self._on_art = False
                self._on_art = None
        return self._on_art

    @property
    def recorded_hiv_result(self):
        """Returns an hiv result based on the last documented result."""
        if not self._recorded_hiv_result:
            # a result from a previous survey is considered record of previous POS result
            recorded_hiv_result = self.previous_value(value_if_pos=POS, value_if_not_pos=None)
            if not recorded_hiv_result:
                try:
                    recorded_hiv_result = self.hiv_test_review_instance.recorded_hiv_result
                except AttributeError:
                    recorded_hiv_result = None
            self._recorded_hiv_result = recorded_hiv_result
        return self._recorded_hiv_result

    @property
    def recorded_hiv_result_date(self):
        """Returns an hiv result based on the last documented result."""
        if not self._recorded_hiv_result_date:
            recorded_hiv_result_date = self.previous_value(
                # attr_if_pos=('hiv_result_datetime', 'date'),
                attr_if_pos=('hiv_result_datetime',),
                value_if_not_pos=None)
            if not recorded_hiv_result_date:
                try:
                    recorded_hiv_result_date = self.hiv_test_review_instance.hiv_test_date
                except AttributeError:
                    recorded_hiv_result_date = None
            self._recorded_hiv_result_date = recorded_hiv_result_date
        return self._recorded_hiv_result_date

    @property
    def todays_cd4_result(self):
        """Returns the CD4 result."""
        if not self._todays_cd4_result:
            try:
                self._todays_cd4_result = int(self.pima_instance.cd4_value)
            except AttributeError:
                self._todays_cd4_result = None
        return self._todays_cd4_result

    @property
    def todays_cd4_result_datetime(self):
        """Returns the CD4 result datetime."""
        if not self._todays_cd4_result_datetime:
            try:
                self._todays_cd4_result_datetime = self.pima_instance.cd4_datetime
            except AttributeError:
                self._todays_cd4_result_datetime = None
        return self._todays_cd4_result_datetime

    @property
    def todays_hiv_result(self):
        """Returns an hiv result from today's test, if it exists."""
        if not self._todays_hiv_result:
            try:
                self._todays_hiv_result = self.hiv_result_instance.hiv_result
            except AttributeError:
                self._todays_hiv_result = None
        return self._todays_hiv_result

    @property
    def todays_hiv_result_datetime(self):
        """Returns an hiv result datetime from today's test, if it exists."""
        if not self._todays_hiv_result_datetime:
            try:
                self._todays_hiv_result_datetime = self.hiv_result_instance.hiv_result_datetime
            except AttributeError:
                self._todays_hiv_result_datetime = None
        return self._todays_hiv_result_datetime

    @property
    def elisa_hiv_result(self):
        """Returns an hiv result from the Elisa result form, if it exists."""
        if not self._elisa_hiv_result:
            try:
                self._elisa_hiv_result = self.elisa_result_instance.hiv_result
            except AttributeError:
                self._elisa_hiv_result = None
        return self._elisa_hiv_result

    @property
    def elisa_hiv_result_datetime(self):
        """Returns an hiv result datetime from Elisa result form, if it exists."""
        if not self._elisa_hiv_result_datetime:
            try:
                self._elisa_hiv_result_datetime = self.elisa_result_instance.hiv_result_datetime
            except AttributeError:
                self._elisa_hiv_result_datetime = None
        return self._elisa_hiv_result_datetime

    @property
    def verbal_hiv_result(self):
        """Returns the hiv result given verbally by the respondent from HivTestingHistory."""
        if not self._verbal_hiv_result:
            try:
                self._verbal_hiv_result = (self.hiv_testing_history_instance.verbal_hiv_result
                                           if self.hiv_testing_history_instance.verbal_hiv_result in [
                                               POS, 'NEG', 'IND'] else None)
            except AttributeError:
                self._verbal_hiv_result = None
        return self._verbal_hiv_result

    @property
    def vl_sample_drawn(self):
        """Returns True if the VL was drawn."""
        if self._vl_sample_drawn is None:
            vl_sample_drawn = self.previous_value(
                attr_if_pos=('vl_sample_drawn', ),
                value_if_not_pos=None)
            if not vl_sample_drawn:
                vl_sample_drawn = True if self.vl_requisition_instance else False
            self._vl_sample_drawn = vl_sample_drawn
        return self._vl_sample_drawn

    @property
    def vl_sample_drawn_datetime(self):
        """Returns the viral load draw datetime from the SubjectRequisition for VL or None."""
        if not self._vl_sample_drawn_datetime:
            vl_sample_drawn_datetime = self.previous_value(
                attr_if_pos=('vl_sample_drawn_datetime', ),
                value_if_not_pos=None)
            if not vl_sample_drawn_datetime:
                try:
                    vl_sample_drawn_datetime = self.vl_requisition_instance.drawn_datetime
                except AttributeError:
                    vl_sample_drawn_datetime = None
            self._vl_sample_drawn_datetime = vl_sample_drawn_datetime
        return self._vl_sample_drawn_datetime

    @property
    def hiv_care_adherence_instance(self):
        """Returns a model instance of HivCareAdherence or None."""
        if not self._hiv_care_adherence_instance:
            try:
                self._hiv_care_adherence_instance = self.models[self.timepoint_key].get(
                    'hiv_care_adherence').objects.get(subject_visit=self.subject_visit)
            except self.models[self.timepoint_key].get('hiv_care_adherence').DoesNotExist:
                self._hiv_care_adherence_instance = None
        return self._hiv_care_adherence_instance

    @property
    def hiv_result_instance(self):
        """Returns a model instance of HivResult or None."""
        if not self._hiv_result_instance:
            try:
                self._hiv_result_instance = self.models[self.timepoint_key].get(
                    'hiv_result').objects.get(
                        subject_visit=self.subject_visit, hiv_result__in=[POS, 'NEG', 'IND', 'Declined'])
            except self.models[self.timepoint_key].get('hiv_result').DoesNotExist:
                self._hiv_result_instance = None
        return self._hiv_result_instance

    @property
    def elisa_result_instance(self):
        if not self._elisa_result_instance:
            try:
                self._elisa_result_instance = self.models[self.timepoint_key].get(
                    'elisa_hiv_result').objects.get(subject_visit=self.subject_visit)
            except self.models[self.timepoint_key].get('elisa_hiv_result').DoesNotExist:
                self._elisa_result_instance = None
        return self._elisa_result_instance

    @property
    def hiv_testing_history_instance(self):
        """Returns a model instance of HivTestingHistory or None."""
        if not self._hiv_testing_history_instance:
            try:
                self._hiv_testing_history_instance = self.models[self.timepoint_key].get(
                    'hiv_testing_history').objects.get(subject_visit=self.subject_visit)
            except self.models[self.timepoint_key].get('hiv_testing_history').DoesNotExist:
                self._hiv_testing_history_instance = None
        return self._hiv_testing_history_instance

    @property
    def hiv_result_documentation_instance(self):
        """Returns a model instance of HivResultDocumentation or None."""
        if not self._hiv_result_documentation_instance:
            try:
                self._hiv_result_documentation_instance = self.models[self.timepoint_key].get(
                    'hiv_result_documentation').objects.get(
                        subject_visit=self.subject_visit, result_recorded__in=[POS, 'NEG', 'IND'])
            except self.models[self.timepoint_key].get('hiv_result_documentation').DoesNotExist:
                self._hiv_result_documentation_instance = None
        return self._hiv_result_documentation_instance

    @property
    def hiv_test_review_instance(self):
        """Returns a model instance of HivTestReview or None."""
        if not self._hiv_test_review_instance:
            try:
                self._hiv_test_review_instance = self.models[self.timepoint_key].get(
                    'hiv_test_review').objects.get(
                        subject_visit=self.subject_visit, recorded_hiv_result__in=[POS, 'NEG', 'IND'])
            except self.models[self.timepoint_key].get('hiv_test_review').DoesNotExist:
                self._hiv_test_review_instance = None
        return self._hiv_test_review_instance

    @property
    def pima_instance(self):
        """Returns a model instance of Pima or None."""
        if not self._pima_instance:
            try:
                self._pima_instance = self.models[self.timepoint_key].get(
                    'pima').objects.get(subject_visit=self.subject_visit, cd4_value__isnull=False)
            except self.models[self.timepoint_key].get('pima').DoesNotExist:
                self._pima_instance = None
        return self._pima_instance

    @property
    def vl_requisition_instance(self):
        """Returns a model instance of the SubjectRequisition for panel VL or None."""
        if not self._vl_requisition_instance:
            try:
                self._vl_requisition_instance = self.models[self.timepoint_key].get(
                    'subject_requisition').objects.get(
                        subject_visit=self.subject_visit, panel__name='Viral Load', is_drawn='Yes')
            except self.models[self.timepoint_key].get('subject_requisition').DoesNotExist:
                pass
        return self._vl_requisition_instance

    @property
    def rbd_sample_drawn(self):
        """Returns True if the VL was drawn."""
        if not self._rbd_sample_drawn:
            rbd_sample_drawn = self.previous_value(
                attr_if_pos=('rbd_sample_drawn', ),
                value_if_not_pos=None)
            if not rbd_sample_drawn:
                rbd_sample_drawn = True if self.vl_requisition_instance else False
            self._rbd_sample_drawn = rbd_sample_drawn
        return self._rbd_sample_drawn

    @property
    def rbd_requisition_instance(self):
        """Returns a model instance of the SubjectRequisition for panel RBD or None."""
        if not self._rbd_requisition_instance:
            try:
                self._rbd_requisition_instance = self.models[self.timepoint_key].get(
                    'subject_requisition').objects.get(
                        subject_visit=self.subject_visit, panel__name='Research Blood Draw', is_drawn='Yes')
            except self.models[self.timepoint_key].get('subject_requisition').DoesNotExist:
                pass
        return self._rbd_requisition_instance
