
UPDATE plot_plot set slug=concat(plot_identifier, '|',  map_area);

UPDATE household_household as HH
LEFT JOIN plot_plot as P ON P.id=HH.plot_id
SET slug=concat(household_identifier, '|', P.slug);

UPDATE household_householdstructure as HHS
LEFT JOIN household_household as HH ON HH.id=HHS.household_id
SET HHS.slug=HH.slug;

UPDATE member_householdmember as HHM
LEFT JOIN household_householdstructure as HHS ON HHS.id=HHM.household_structure_id
SET HHM.slug=CONCAT(HHM.subject_identifier, '|', HHM.internal_identifier, '|', HHS.slug);

UPDATE bcpp_subject_subjectconsent as C
LEFT JOIN member_householdmember as HHM ON HHM.id=C.household_member_id
SET C.slug=CONCAT(C.subject_identifier, '|', HHM.slug);

UPDATE bcpp_subject_subjectrequisition as R
LEFT JOIN bcpp_subject_subjectvisit as V on V.id=R.subject_visit_id
LEFT JOIN member_householdmember as HHM ON V.household_member_id=HHM.id
SET R.slug=CONCAT(V.subject_identifier, '|', R.requisition_identifier, '|',
CONCAT(substring(R.requisition_identifier, 1, 4),'-', substring(R.requisition_identifier, 5, 4)),'|',
R.panel_name, '|', R.identifier_prefix, '|', HHM.slug);
