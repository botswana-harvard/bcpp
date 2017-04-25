from edc_fabric import fabfile as common

from .deploy import deploy_centralserver, deploy_client, deploy_nodeserver
from .utils import restore_media_folder
from .update import query_tx_task
from .local_base_env import load_base_env

load_base_env()
