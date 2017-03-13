LOAD DATA INFILE '/Users/erikvw/bcpp_201703/new/bcpp_subject/subjectconsent.csv'
INTO TABLE edc_migrated.bcpp_subject_subjectconsent
CHARACTER SET utf8
FIELDS TERMINATED BY '|' ENCLOSED BY '"'
LINES TERMINATED BY '\n' STARTING BY ''
IGNORE 1 LINES
(@comment,confirm_identity,hostname_created,last_name,may_store_samples,@consent_datetime,hostname_modified,is_minor,witness_name,is_literate,subject_type,consent_copy,user_created,@id,marriage_certificate,first_name,@subject_identifier_as_pk,is_dob_estimated,verified_by,@user_modified,@is_signed,@is_verified_datetime,subject_identifier_aka,version,citizen,legal_marriage,@is_verified,is_incarcerated,revision,consent_reviewed,assessment_score,study_questions,sid,subject_identifier,@marriage_certificate_no,identity,language,@created,identity_type,@household_member_id,@modified,consent_signature,dm_comment,gender,@dob,survey_schedule,guardian_name,initials,consent_identifier)
SET 
dob = nullif(@dob, ''),
id = replace(@id,'-',''),
subject_identifier_as_pk = REPLACE(@subject_identifier_as_pk,'-',''),
household_member_id = REPLACE(@household_member_id,'-',''),
consent_datetime = NULLIF(STR_TO_DATE(@consent_datetime, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
is_verified_datetime = NULLIF(STR_TO_DATE(@is_verified_datetime, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
created = NULLIF(STR_TO_DATE(@created, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00"),
modified = NULLIF(STR_TO_DATE(@modified, '%Y-%m-%d %H:%i:%s+00:00'), "0000-00-00");
