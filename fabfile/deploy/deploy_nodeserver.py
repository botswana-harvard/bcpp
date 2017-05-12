from fabric.api import task
from .deploy import deploy


@task
def deploy_nodeserver(**kwargs):
    conf_filename = 'bootstrap_nodeserver.conf'
    deploy(conf_filename=conf_filename, **kwargs)
