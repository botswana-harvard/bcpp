from ...deploy import deploy_client as _deploy_client

from fabric.api import task


@task
def r0136(*requirements_list, **kwargs):
    """Release 0.1.36.

        fab -P -R mmankgodi deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.36,map_area=oodi --user=django \
            skip_update_os=True, skip_db=True, skip_restore_db=True, skip_mysql=True, skip_python=True, skip_web=True, skip_collectstatic=True, skip_bash_config=True, skip_keys=True

    """
    _deploy_client(requirements_list=requirements_list, **kwargs)
