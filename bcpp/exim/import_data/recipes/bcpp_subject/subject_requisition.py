import pandas as pd
import numpy as np

# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices


def panel_name(value):
    panels = {
        6: 'Clinic Viral Load',
        4: 'ELISA',
        3: 'Microtube',
        1: 'Research Blood Draw',
        5: 'Venous (HIV)',
        2: 'Viral Load',
        7: 'Viral Load (Abbott)',
        8: 'Viral Load (POC)',
    }
    if pd.isnull(value):
        return np.NaN
    elif value not in panels.keys():
        raise ImportError('Invalid panel id. Got {}'.format(value))
    return panels.get(value)


def study_site_name(value):
    study_sites = {
        '7a8f443e-585c-47ce-bc51-87ebc3ff9079': 'bhp',
        '20ba1ef1-a0db-4ce6-9ef1-1a657792e85e': 'bokaa',
        '75e13fd0-cd67-4f03-a76c-8f1bb2e3f02b': 'digawana',
        '3d515a37-348b-4a8d-9cd3-251a5ef011fc': 'gumare',
        'c764562f-00d5-478d-94bb-c5c12bc11b99': 'gweta',
        '8136de34-b505-4ede-b67c-4e19daa77ca2': 'lentsweletau',
        '8149d201-44d7-4c11-b55d-2725026457b9': 'lerala',
        '350576fb-cc8f-40c5-b193-612409bbb1fc': 'letlhakeng',
        '76e77e73-cc8c-4a34-a47c-48f8d077f847': 'masunga',
        '376a103e-f6c4-45f6-820b-8fe26bb3699d': 'mathangwane',
        '5ee9650b-ab1c-4792-98e6-add6108803ee': 'maunatlala',
        'ad295aa0-7d39-49d8-9776-71636189f43f': 'metsimotlhabe',
        '77bc150d-9995-4628-9a5f-121b8790f018': 'mmadinare',
        '07ea26f2-ff34-4f05-8b43-cd72d982f3d4': 'mmandunyane',
        '75ae58fb-31c1-490e-8476-52249b43522f': 'mmankgodi',
        'eab470af-eaa5-46c7-9a56-cd4b86f1d69f': 'mmathethe',
        'f552d77d-9d14-4227-987f-9a02a8c1ced0': 'molapowabojang',
        'bb9089f5-82de-4d95-8f9d-0848f889141e': 'nata',
        'bed5567f-7585-489a-ba47-d1a4b2f313b4': 'nkange',
        '5cb384bc-ad3c-46b2-acfb-c24f0679ebbe': 'oodi',
        'd4331980-e7c8-11e3-94ee-a82066234239': 'otse',
        'd6fde611-1828-43ee-94db-8b227e212dc3': 'rakops',
        '3e825b42-8080-451b-a6d4-04b8fadd230f': 'ramokgonami',
        '2fed1266-65f5-4fa1-a873-b7f3382ca43b': 'ranaka',
        '3752edbf-5721-445c-9fba-50a59531505a': 'sebina',
        'a1c263e6-6738-4308-8131-faa9c72a7452': 'sefhare',
        'a1b5c312-2edd-4f64-a698-38590ee67ab9': 'sefophe',
        'cddde46a-4742-44e8-acbf-b141396c6bed': 'shakawe',
        'f9ea084a-d68f-44a2-8b29-23c5c47f4113': 'shoshong',
        '9b3794b9-a467-46a0-9973-acfd2686d301': 'tati_siding',
        '4dda6e3f-907f-4acb-8c7f-14e9768bf3cd': 'test_community',
        '023da3b2-6e12-4944-820d-ca7d7d6a17aa': 'tsetsebjwe',
    }
    if pd.isnull(value):
        return np.NaN
    elif value not in study_sites.keys():
        raise ImportError('Invalid site_id. Got {}'.format(value))
    return study_sites.get(value)


def study_site(value):
    site_codes = {
        '7a8f443e-585c-47ce-bc51-87ebc3ff9079': '00',
        '4dda6e3f-907f-4acb-8c7f-14e9768bf3cd': '01',
        '2fed1266-65f5-4fa1-a873-b7f3382ca43b': '11',
        '75e13fd0-cd67-4f03-a76c-8f1bb2e3f02b': '12',
        'f552d77d-9d14-4227-987f-9a02a8c1ced0': '13',
        'd4331980-e7c8-11e3-94ee-a82066234239': '14',
        '350576fb-cc8f-40c5-b193-612409bbb1fc': '15',
        '8136de34-b505-4ede-b67c-4e19daa77ca2': '16',
        '20ba1ef1-a0db-4ce6-9ef1-1a657792e85e': '17',
        '5cb384bc-ad3c-46b2-acfb-c24f0679ebbe': '18',
        '75ae58fb-31c1-490e-8476-52249b43522f': '19',
        'eab470af-eaa5-46c7-9a56-cd4b86f1d69f': '20',
        '8149d201-44d7-4c11-b55d-2725026457b9': '21',
        'a1b5c312-2edd-4f64-a698-38590ee67ab9': '22',
        '5ee9650b-ab1c-4792-98e6-add6108803ee': '23',
        '3e825b42-8080-451b-a6d4-04b8fadd230f': '24',
        'f9ea084a-d68f-44a2-8b29-23c5c47f4113': '25',
        '77bc150d-9995-4628-9a5f-121b8790f018': '26',
        'bed5567f-7585-489a-ba47-d1a4b2f313b4': '27',
        '3752edbf-5721-445c-9fba-50a59531505a': '28',
        'ad295aa0-7d39-49d8-9776-71636189f43f': '29',
        '9b3794b9-a467-46a0-9973-acfd2686d301': '30',
        '376a103e-f6c4-45f6-820b-8fe26bb3699d': '31',
        '07ea26f2-ff34-4f05-8b43-cd72d982f3d4': '32',
        'd6fde611-1828-43ee-94db-8b227e212dc3': '33',
        'c764562f-00d5-478d-94bb-c5c12bc11b99': '34',
        '3d515a37-348b-4a8d-9cd3-251a5ef011fc': '35',
        'cddde46a-4742-44e8-acbf-b141396c6bed': '36',
        '76e77e73-cc8c-4a34-a47c-48f8d077f847': '37',
        'bb9089f5-82de-4d95-8f9d-0848f889141e': '38',
        'a1c263e6-6738-4308-8131-faa9c72a7452': '39',
        '023da3b2-6e12-4944-820d-ca7d7d6a17aa': '40',
    }
    if pd.isnull(value):
        return np.NaN
    elif value not in site_codes.keys():
        raise ImportError('Invalid site_code. Got {}'.format(value))
    return site_codes.get(value)

df_drop_columns = ['community',
                   'protocol', 'priority',
                   'is_lis', 'subject_identifier']

df_add_columns = []

df_copy_columns = {
    'study_site_name': 'site_id',
    'packed_datetime': 'is_labelled_datetime'}

df_rename_columns = {
    'specimen_identifier': 'identifier_prefix',
    'site_id': 'study_site',
    'aliquot_type_id': 'specimen_type',
    'item_count_total': 'item_count',
    'panel_id': 'panel_name',
    'is_receive': 'received',
    'is_receive_datetime': 'received_datetime',
    'is_packed': 'packed',
    'is_labelled': 'processed',
    'is_labelled_datetime': 'processed_datetime'}

df_apply_functions = {
    'item_type': lambda row: common_choices(row['item_type']),
    'panel_name': lambda row: panel_name(row['panel_name']),
    'study_site': lambda row: study_site(row['study_site']),
    'study_site_name': lambda row: study_site_name(row['study_site_name']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.subjectrequisition',
    old_model_name='bcpp_lab.subjectrequisition',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_copy_columns=df_copy_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
