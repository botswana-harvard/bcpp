
# TODO

* import audit trail
* update slug fields
* household_structure.survey_schedule
    * done: fix survey_schedule in household_structure (test_community -> real community)
    * verify survey_schedule_object returns correct community
* review identifier history table to prevent duplicate identifiers
    * plot
    * household
    * etc ...
* check survey_schedule field is populated on all models that use it
* household_member : calculate citizen, non-citizen
    

# ISSUES

## Plot

    ```sql
    update plot_plot set location_name='plot' where confirmed=1;
    ```
    
## Household Member

* household member 63050 reduced to 62863 after removing duplicates
    on key (first_name, initials, household_structure).
* added back 17 to match with consents
* update survey_schedule in HHM from HHS:

   update survey schedule from HHS
   
    ```sql
    UPDATE member_householdmember HHM
    JOIN household_householdstructure HHS ON HHM.household_structure_id = HHS.id
    SET HHM.survey_schedule = HHS.survey_schedule;
    ```

   update household_identifier from HH

    ```sql
    UPDATE member_householdmember HHM
    JOIN household_householdstructure HHS ON HHM.household_structure_id = HHS.id
    JOIN household_household HH ON HHS.household_id = HH.id
    SET HHM.household_identifier = HH.household_identifier;
    ```

   List all household identifiers from HH and HHM
   
    ```sql
    SELECT hh.household_identifier, hhm.household_identifier
    FROM member_householdmember as hhm
    LEFT JOIN household_householdstructure as hhs on hhm.household_structure_id=hhs.id
    LEFT JOIN household_household as hh on hhs.household_id=hh.id;
    ```

* update subject_identifier
    
   Find all occurences of `subject_identifier`
   
    ```sql
    SELECT table_name,table_schema, column_name
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE table_schema='edc_migrated' AND column_name='subject_identifier';
    ```

   update in `member_householdmember`
   
    ```sql
    UPDATE member_householdmember HHM
    LEFT JOIN edc_registration_registeredsubject AS REG
    ON HHM.internal_identifier=REG.registration_identifier 
    SET HHM.subject_identifier=IFNULL(REG.subject_identifier, replace(uuid(),'-',''));

    SELECT distinct r.subject_identifier
    FROM member_householdmember as hhm LEFT JOIN edc_registration_registeredsubject AS r
    ON hhm.internal_identifier=r.registration_identifier 
    WHERE SUBSTRING(r.subject_identifier, 1, 4)='066-';
    ```

##Identifiers

###identifier_model

   subjects

    ```sql
    INSERT INTO edc_identifier_identifiermodel (id,name,subject_type,model,identifier,
    device_id,sequence_number,created,modified,user_created,user_modified,
    hostname_created,hostname_modified,
    protocol_number,study_site,revision)
    SELECT
    REPLACE(uuid(),'-','') as id,
    'subjectidentifier' as name,
    'subject' as subject_type,
    'bcpp_subject.subjectconsent' as model,
    subject_identifier as identifier,
    substring(subject_identifier, 7, 2) as device_id,
    CAST(substring(subject_identifier, 9, 4) AS UNSIGNED) as sequence_number,
    created as created,
    modified as modified,
    user_created as user_created,
    user_modified as user_modified,
    hostname_created as hostname_created,
    hostname_modified as hostname_modified,
    substring(subject_identifier, 1, 3) as protocol_number,
    substring(subject_identifier, 5, 2) as study_site,
    revision as revision
    FROM edc_registration_registeredsubject where SUBSTRING(subject_identifier, 1, 4)='066-';
    ```
   plots
   
    ```sql
    INSERT INTO edc_identifier_identifiermodel (id,name,subject_type,model,identifier,
    device_id,sequence_number,created,modified,user_created,user_modified,
    hostname_created,hostname_modified,
    protocol_number,study_site,revision)
    SELECT
    REPLACE(uuid(),'-','') as id,
    'plot_identifier' as name,
    NULL as subject_type,
    'plot.plot' as model,
    plot_identifier as identifier,
    '99' as device_id,
    CAST(substring(plot_identifier, 3, 4) AS UNSIGNED) as sequence_number,
    created as created,
    modified as modified,
    user_created as user_created,
    user_modified as user_modified,
    hostname_created as hostname_created,
    hostname_modified as hostname_modified,
    '066' as protocol_number,
    substring(plot_identifier, 1, 2) as study_site,
    revision as revision
    FROM plot_plot;
    ```
   
   
## REGISTERED_SUBJECT

* add back 44 missing registered subject records    

    ```sql
    INSERT INTO edc_registration_registeredsubject 
    (subject_type, id, subject_identifier_as_pk, registration_identifier, first_name, initials, gender, created, modified, registration_datetime,
    subject_identifier, identity_or_pk, user_created, user_modified, hostname_created, hostname_modified, dm_comment) 
    SELECT 'subject', replace(uuid(),'-',''), replace(uuid(),'-',''), HHM.id, HHM.first_name, HHM.initials, HHM.gender, HHM.created, now(), HHM.created,
    replace(uuid(),'-',''), replace(uuid(),'-',''), HHM.user_created, 'erikvw', HHM.hostname_created, HHM.hostname_modified, 'created erikvw'
    FROM member_householdmember AS hhm
    LEFT JOIN edc_registration_registeredsubject AS reg 
    ON hhm.internal_identifier=reg.registration_identifier
    WHERE reg.id is NULL;
    ```

* Duplicate RegisteredSubjects

    Cannot update registered subject with a duplicate 'identity'. Got 171523610.
    Cannot update registered subject with a duplicate 'identity'. Got 104224018.
    Cannot update registered subject with a duplicate 'identity'. Got 565616307.
    Cannot update registered subject with a duplicate 'identity'. Got 587123019.
    Cannot update registered subject with a duplicate 'identity'. Got 848526010.
    Cannot update registered subject with a duplicate 'identity'. Got 683429315.
    Cannot update registered subject with a duplicate 'identity'. Got 866129604.
    Cannot update registered subject with a duplicate 'identity'. Got 550924510.
    Cannot update registered subject with a duplicate 'identity'. Got 884820716.
    Cannot update registered subject with a duplicate 'identity'. Got 613024905.
    Cannot update registered subject with a duplicate 'identity'. Got 637729102.
    Cannot update registered subject with a duplicate 'identity'. Got 943614203.
    Cannot update registered subject with a duplicate 'identity'. Got 477620700.
    Cannot update registered subject with a duplicate 'identity'. Got 826522206.
    Cannot update registered subject with a duplicate 'identity'. Got 595525509.
    Cannot update registered subject with a duplicate 'identity'. Got 646716109.
    Cannot update registered subject with a duplicate 'identity'. Got 580810303.
    Cannot update registered subject with a duplicate 'identity'. Got 788016800.
    Cannot update registered subject with a duplicate 'identity'. Got 227026801.
    Cannot update registered subject with a duplicate 'identity'. Got 087322802.
    Cannot update registered subject with a duplicate 'identity'. Got 895513705.
    Cannot update registered subject with a duplicate 'identity'. Got 387222600.
    Cannot update registered subject with a duplicate 'identity'. Got 365129005.
    Cannot update registered subject with a duplicate 'identity'. Got 306729821.
    Cannot update registered subject with a duplicate 'identity'. Got 029715401.
    Cannot update registered subject with a duplicate 'identity'. Got 427823914.
    Cannot update registered subject with a duplicate 'identity'. Got 381925302.

* registered subject with subjectidentifier but no consent (clinic consents?)

    ```sql
    SELECT r.subject_identifier FROM edc_registration_registeredsubject as r
    LEFT JOIN bcpp_subject_subjectconsent as c ON r.subject_identifier=c.subject_identifier
    WHERE c.id is NULL and SUBSTRING(r.subject_identifier, 1, 4) = '066-';
    ```

## MEMBER STATUS MODELS

* some are model pair of model + model_entry
* member.enrollmentchecklist ... 13791/13791.  11 errors.
* member.enrolmentloss ... 563/563.  1 error.
    one orphaned record could not be imported for
    household_member_id='d5c5b93e-6d52-4837-aa47-2964a664ae9c'
    # member.refusedmember ... 1560/1560.  0 error.
    added missing REASON option
    ('I already know my status', ('I already know my status')),
* member.deceasedmember NOT IMPORTED!!!

## BCPP_SUBJECT

### bcpp_subject.subjectconsent

    ```sql
    subject_identifier_as_pk should be UUIDField() not 36 CharField.  use uuid4().hex for storage
    identity_or_pk
    ```

### Appointment
* update survey_schedule

    ```sql
    UPDATE bcpp_subject_appointment APPT
    JOIN member_householdmember HHM ON APPT.household_member_id = HHM.id
    SET APPT.survey_schedule = HHM.survey_schedule;
    ```
* update survey
    
    ```sql
    UPDATE bcpp_subject_appointment SET survey=CONCAT(SUBSTRING(survey_schedule,1,23), '.bhs', SUBSTRING(survey_schedule,24,100)) WHERE schedule_name='bhs_schedule';
    UPDATE bcpp_subject_appointment SET survey=CONCAT(SUBSTRING(survey_schedule,1,23), '.ahs', SUBSTRING(survey_schedule,24,100)) WHERE schedule_name='ahs_schedule';
    ```
    
* update visit_schedule_name

    ```sql
    UPDATE bcpp_subject_appointment SET visit_schedule_name='visit_schedule_bhs'
    WHERE schedule_name='bhs_schedule';
    UPDATE bcpp_subject_appointment SET visit_schedule_name='visit_schedule_ahs'
    WHERE schedule_name='ahs_schedule';
    ```

* update subject_identifier

    ```sql
    UPDATE bcpp_subject_appointment APPT
    JOIN member_householdmember HHM ON APPT.household_member_id = HHM.id
    SET APPT.subject_identifier = HHM.subject_identifier;
    ```

### subject visit

* update subject_identifier
    
    ```sql
    UPDATE bcpp_subject_subjectvisit V
    JOIN bcpp_subject_appointment APPT ON V.appointment_id = APPT.id
    SET V.subject_identifier = APPT.subject_identifier;
    ```

* update survey_schedule
    
    ```sql
    UPDATE bcpp_subject_subjectvisit V
    JOIN bcpp_subject_appointment APPT ON V.appointment_id = APPT.id
    SET V.survey_schedule = APPT.survey_schedule;

    UPDATE bcpp_subject_subjectvisit V
    JOIN bcpp_subject_appointment APPT ON V.appointment_id = APPT.id
    SET 
    V.survey_schedule = APPT.survey_schedule,
    V.survey=APPT.survey,
    V.visit_schedule_name=APPT.visit_schedule_name,
    V.schedule_name=APPT.schedule_name,
    V.visit_code=APPT.visit_code;
    ```

### subject_locator

    ```sql
    UPDATE bcpp_subject_subjectlocator L
    JOIN edc_registration_registeredsubject R ON L.subject_identifier = R.id
    SET L.subject_identifier = R.subject_identifier;
    ```


## Enrollment Models

Populate enrollment / disenrollment

## LIST DATA

    ```sql
    SELECT 'hostname_created', 'name', 'short_name', 'created', 'user_modified',
    'modified', 'hostname_modified', 'version', 'display_index', 'user_created',
    'field_name','id','revision'
    UNION ALL
    SELECT hostname_created, name, short_name, created, user_modified,
    modified, hostname_modified, version, display_index, user_created,
    field_name,id,revision INTO OUTFILE '/Users/erikvw/bcpp_201703/bcpp_list_electricalappliances.csv'
    CHARACTER SET UTF8
    FIELDS TERMINATED BY '|' ENCLOSED BY ''
    LINES TERMINATED BY '\n'
    FROM bhp066.bcpp_list_electricalappliances;
    ```