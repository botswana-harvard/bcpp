import sys

if 'fab' in sys.argv[0]:
    from edc_fabric import fabfile as common
    from .deploy import (
        deploy_centralserver, deploy_client, deploy_nodeserver, deployment_host)
    from .local_base_env import load_base_env
    from .utils import restore_media_folder, generate_anonymous_transactions
    from .utils import (
        load_keys_bcpp, check_repo_status, install_dependency_specific_tag,
        install_dependency_not_in_requirements)

    from .update.r0_1_36 import deploy_client as r0136
    from .update import r0134, r0135

    load_base_env()
