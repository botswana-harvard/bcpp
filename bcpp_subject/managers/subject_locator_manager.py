from .scheduled_model_manager import ScheduledModelManager


class SubjectLocatorManager(ScheduledModelManager):

    def previous(self, household_member):
        """Returns the previous subject locator instance or None"""
        previous = None
        try:
            previous = self.filter(
                subject_visit__household_member__internal_identifier=household_member.internal_identifier
            ).exclude(subject_visit__household_member__pk=household_member.pk).order_by(
                '-subject_visit__report_datetime')[0]
        except IndexError:
            pass
        return previous
