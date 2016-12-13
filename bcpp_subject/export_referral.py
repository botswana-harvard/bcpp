from bcpp_subject.models.subject_locator import SubjectLocator
from django.db.models.aggregates import Max


class ExportReferral:
    # TODO: does not work, code was taken from the subject referral model
    @property
    def ready_to_export_transaction(self):
        """Evaluates to True only if the instance has a referral code to avoid
        exporting referral data on someone who is not yet referred.

        This method is used by the model manager ExportHistoryManager.

        The assumption is that the referral instance CANNOT be created without
        an existing SubjectLocator instance.

        The subject's subject_locator instance is exported as well.

        If there is no subject_locator, the subject_referral is not exported.

        ...see_also:: SubjectReferral"""
        export_subject_referral = False
        try:
            # check if there is a subject locator.
            # Cannot export this referral without the Subject Locator.
            subject_locator = SubjectLocator.objects.get(
                subject_visit__appointment__registered_subject=self.subject_visit.appointment.registered_subject)
            # check if referral is complete
            if (self.referral_code and self.referral_appt_date and self.referral_clinic_type):
                try:
                    # export the subject locator
                    SubjectLocator.export_history.export_transaction_model.objects.get(
                        object_name=SubjectLocator._meta.object_name,
                        tx_pk=subject_locator.pk,
                        export_change_type='I')
                    SubjectLocator.export_history.serialize_to_export_transaction(
                        subject_locator, 'U', 'default', force_export=True)
                except SubjectLocator.export_history.export_transaction_model.DoesNotExist:
                    SubjectLocator.export_history.serialize_to_export_transaction(
                        subject_locator, 'I', 'default', force_export=True)
                except SubjectLocator.export_history.export_transaction_model.MultipleObjectsReturned:
                    SubjectLocator.export_history.serialize_to_export_transaction(
                        subject_locator, 'U', 'default', force_export=True)
                finally:
                    export_subject_referral = True
            else:
                # there is no referral ready yet, need to send a Delete to the
                # export tx receipient.
                # is the last transaction not a D? if not, add one.
                try:
                    aggr = SubjectLocator.export_history.export_transaction_model.objects.filter(
                        pk=subject_locator.pk).aggregate(Max('timestamp'), )
                    SubjectLocator.export_history.export_transaction_model.objects.get(
                        timestamp=aggr.get('timestamp__max'),
                        export_change_type='D')
                except SubjectLocator.export_history.export_transaction_model.DoesNotExist:
                    SubjectLocator.export_history.serialize_to_export_transaction(subject_locator, 'D', None)
        except SubjectLocator.DoesNotExist:
            pass
        return export_subject_referral

