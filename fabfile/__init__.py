from edc_fabric import fabfile as common

from .deploy import deploy_centralserver, deploy_client, deploy_nodeserver, deployment_host
from .local_base_env import load_base_env
from .utils import restore_media_folder

load_base_env()
