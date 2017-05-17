from fabric.api import task
from .deploy import deploy


@task
def deploy_nodeserver(*requirements_list, **kwargs):
    conf_filename = 'bootstrap_nodeserver.conf'
    deploy(requirements_list=requirements_list, conf_filename=conf_filename, **kwargs)
