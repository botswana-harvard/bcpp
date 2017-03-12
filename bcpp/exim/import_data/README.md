
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

## Household Member

* household member 63050 reduced to 62863 after removing duplicates
    on key (first_name, initials, household_structure).
* added back 17 to match with consents


## REGISTERED_SUBJECT

### Duplicate RegisteredSubjects

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


### registered subject with subjectidentifier but no consent

    SELECT r.subject_identifier FROM edc_registration_registeredsubject as r
    LEFT JOIN bcpp_subject_subjectconsent as c ON r.subject_identifier=c.subject_identifier
    WHERE c.id is NULL and SUBSTRING(r.subject_identifier, 1, 4) = '066-';

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

    subject_identifier_as_pk should be UUIDField() not 36 CharField.  use uuid4().hex for storage
    identity_or_pk

## LIST DATA
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