import sys

if 'fab' in sys.argv[0]:
    from edc_fabric import fabfile as common

    from .deploy import (
        deploy_centralserver, deploy_client, deploy_nodeserver, deployment_host)
    from .local_base_env import load_base_env
    from .utils import (
        restore_media_folder, generate_anonymous_transactions, check_repo_status)

    from .update.r0_1_36 import deploy_client as r0136
    from .update import r0134, r0135

load_base_env()
