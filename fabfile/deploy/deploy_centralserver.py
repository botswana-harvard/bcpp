from fabric.api import task

from .deploy import deploy


@task
def deploy_centralserver(**kwargs):
    """

        fab -H bhp066 deploy.deploy_centralserver:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.26,map_area=botswana --user=django

    """

    conf_filename = 'bootstrap_centralserver.conf'
    deploy(conf_filename=conf_filename, **kwargs)
