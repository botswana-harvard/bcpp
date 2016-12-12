from datetime import datetime


from edc_export.classes import ExportAsCsv

from .choices import REFERRAL_CODES
from .models import SubjectReferral


def update_referrals(modeladmin, request, queryset):
    for obj in queryset:
        try:
            bhs_referral_code = SubjectReferral.objects.get(subject_visit=obj.subject_visit).referral_code
            obj.bhs_referral_code = bhs_referral_code
            obj.save(update_fields=['bhs_referral_code'])
        except SubjectReferral.DoesNotExist:
            pass
update_referrals.short_description = "Update selected referrals"


def export_referrals_for_cdc_action(description="Export Referrals for CDC (Manual)", fields=None, exclude=None,
                                    extra_fields=None, header=True, track_history=True, show_all_fields=True,
                                    delimiter=None, encrypt=True, strip=False):
    """Filters then exports a queryset from admin.

    The post admin filtering takes out:
      * out any referrals with an invalid or blank code.
      * any referrals NOT covered by an appointment that is DONE (appt_status=DONE).
      * any referrals that were previously exported (exported=True).

    """
    def export(modeladmin, request, queryset):
        referral_code_list = [key for key, _ in REFERRAL_CODES if not key == 'pending']
        queryset = queryset.filter(
            referral_code__in=referral_code_list, in_clinic_flag=False)
        export_as_csv = ExportAsCsv(
            queryset,
            modeladmin=modeladmin,
            fields=fields,
            exclude=exclude,
            extra_fields=extra_fields,
            header=header,
            track_history=track_history,
            show_all_fields=show_all_fields,
            delimiter=delimiter,
            export_datetime=datetime.now(),
            encrypt=encrypt,
            strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export


def export_locator_for_cdc_action(description="Export Locator for CDC (Manual)",
                                  fields=None, exclude=None, extra_fields=None,
                                  header=True, track_history=True, show_all_fields=True,
                                  delimiter=None, encrypt=True, strip=False):

    def export(modeladmin, request, queryset):
        """Filter locator for those referred and data not yet seen in clinic (in_clinic_flag=False)."""
        referral_code_list = [key for key, _ in REFERRAL_CODES if not key == 'pending']
        referred_subject_identifiers = [dct.get('subject_visit__subject_identifier')
                                        for dct in SubjectReferral.objects.values(
                                            'subject_visit__subject_identifier').filter(
                                                referral_code__in=referral_code_list, in_clinic_flag=False)]
        queryset = queryset.filter(subject_visit__subject_identifier__in=referred_subject_identifiers)
        export_as_csv = ExportAsCsv(
            queryset,
            modeladmin=modeladmin,
            fields=fields,
            exclude=exclude,
            extra_fields=extra_fields,
            header=header,
            track_history=track_history,
            show_all_fields=show_all_fields,
            delimiter=delimiter,
            export_datetime=datetime.now(),
            encrypt=encrypt,
            strip=strip)
        return export_as_csv.write_to_file()

    export.short_description = description

    return export
