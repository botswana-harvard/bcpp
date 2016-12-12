from .scheduled_model_manager import ScheduledModelManager


class ViralLoadResultManager(ScheduledModelManager):

    def get_by_natural_key(self, sample_id):
        return self.get(sample_id=sample_id)
