from .scheduled_model_manager import ScheduledModelManager


class TbSymptomsManager(ScheduledModelManager):

    def get_symptoms(self, subject_visit):
        symptoms = []
        try:
            obj = self.get(subject_visit=subject_visit)
            if obj.cough == 'Yes':
                symptoms.append('cough')
            if obj.lymph_nodes == 'Yes':
                symptoms.append('lymph_nodes')
            if obj.night_sweat == 'Yes':
                symptoms.append('night_sweat')
            if obj.cough_blood == 'Yes':
                symptoms.append('cough_blood')
            if obj.weight_loss == 'Yes':
                symptoms.append('weight_loss')
            symptoms.sort()
        except self.model.DoesNotExist:
            pass
        return ', '.join(symptoms)
