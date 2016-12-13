from edc_lab.aliquot.aliquot_type import AliquotType
from edc_lab.aliquot.processing_profile import ProcessingProfile
from edc_lab.lab_profile import LabProfile
from edc_lab.requisition.requisition_panel import RequisitionPanel
from edc_lab.site_lab_profiles import site_lab_profiles


lab_profile = LabProfile('bcpp_lab')

pl = AliquotType('Plasma', 'PL', '36')
lab_profile.add_aliquot_type(pl)

bc = AliquotType('Buffy Coat', 'BC', '12')
lab_profile.add_aliquot_type(bc)

wb = AliquotType('Whole Blood', 'WB', '02')
wb.add_derivative(bc)
wb.add_derivative(pl)
lab_profile.add_aliquot_type(wb)

viral_load_processing = ProcessingProfile('viral_load', wb)
viral_load_processing.add_process(pl, 4)
viral_load_processing.add_process(bc, 3)
lab_profile.add_processing_profile(viral_load_processing)

pbmc_processing = ProcessingProfile('pbmc', wb)
pbmc_processing.add_process(pl, 4)
lab_profile.add_processing_profile(pbmc_processing)

viral_load_panel = RequisitionPanel('Viral Load', wb)  # link this to the visit_schedule
viral_load_panel.processing_profile = viral_load_processing
lab_profile.add_panel(viral_load_panel)

rdb_panel = RequisitionPanel('Research Blood Draw', wb)  # link this to the visit_schedule
lab_profile.add_panel(rdb_panel)

site_lab_profiles.register('bcpp_lab.subjectrequisition', lab_profile)
