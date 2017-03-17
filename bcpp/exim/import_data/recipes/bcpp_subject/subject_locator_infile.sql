LOAD DATA INFILE '/Users/erikvw/bcpp_201703/new/bcpp_subject/subjectlocator.csv'
INTO TABLE edc_migrated.bcpp_subject_subjectlocator
CHARACTER SET utf8
FIELDS TERMINATED BY '|' ENCLOSED BY '"'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES
(alt_contact_cell,alt_contact_cell_number,alt_contact_name,alt_contact_rel,alt_contact_tel,consent_version,contact_cell,contact_name,contact_phone,contact_physical_address,contact_rel,@created,has_alt_contact,home_visit_permission,hostname_created,hostname_modified,@id,mail_address,may_call_work,may_contact_someone,may_follow_up,may_sms_follow_up,@modified,other_alt_contact_cell,physical_address,@report_datetime,revision,subject_cell,subject_cell_alt,subject_identifier,subject_phone,subject_phone_alt,subject_work_phone,subject_work_place,user_created,user_modified)
SET 
id = replace(@id,'-',''),
created = NULLIF(STR_TO_DATE(@created, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
modified = NULLIF(STR_TO_DATE(@modified, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
report_datetime = NULLIF(STR_TO_DATE(@report_datetime, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00");
