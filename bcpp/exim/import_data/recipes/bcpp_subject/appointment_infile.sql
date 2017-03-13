
SET foreign_key_checks = 0;

LOAD DATA INFILE '/Users/erikvw/bcpp_201703/new/bcpp_subject/appointment.csv'
INTO TABLE edc_migrated.bcpp_subject_appointment
CHARACTER SET utf8
FIELDS TERMINATED BY '|' ENCLOSED BY '"'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES
(@appt_close_datetime,@appt_datetime,appt_reason,appt_status,appt_type,@comment,@created,hostname_created,hostname_modified,@household_member_id,@id,is_confirmed,@modified,revision,schedule_name,subject_identifier,@survey_schedule,timepoint,@timepoint_datetime,@user_created,@user_modified,visit_code,visit_instance,visit_schedule_name)
SET 
id = replace(@id,'-',''),
comment=IFNULL(@comment, ''),
survey_schedule=IFNULL(@survey_schedule, ''),
user_created=IFNULL(@user_created, 'admin'),
user_modified=IFNULL(@user_modified, 'admin'),
household_member_id = replace(@household_member_id,'-',''),
created = NULLIF(STR_TO_DATE(@created, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
modified = NULLIF(STR_TO_DATE(@modified, '%Y-%m-%d %H:%i:%s+00:00'), NULL),
appt_close_datetime = NULLIF(STR_TO_DATE(@appt_close_datetime, '%Y-%m-%d %H:%i:%s+00:00'), NULL),
appt_datetime = NULLIF(STR_TO_DATE(@appt_datetime, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
timepoint_datetime = NULLIF(STR_TO_DATE(@timepoint_datetime, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00");

SET foreign_key_checks = 1;