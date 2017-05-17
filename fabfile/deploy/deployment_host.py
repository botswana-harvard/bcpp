from fabric.api import execute, task

from edc_fabric.fabfile import prepare_deployment_host, prepare_update_host


@task
def deployment_host(*requirements_list, bootstrap_path=None, release=None, skip_clone=None, skip_pip_download=None,
                    use_branch=None, bootstrap_branch=None, update=None):
    """
    Example:

        brew update && fab -H localhost deploy.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,use_branch=True,bootstrap_branch=develop,skip_pip_download=True,skip_clone=True

    """
    if not update:
        execute(prepare_deployment_host,
                bootstrap_path=bootstrap_path,
                release=release,
                skip_clone=skip_clone,
                skip_pip_download=skip_pip_download,
                use_branch=use_branch,
                bootstrap_branch=bootstrap_branch)
    else:
        """ fab -H localhost deploy.deployment_host:bcpp-subject,edc-lab,plot,bootstrap_path=/Users/imosweu/source/bcpp/fabfile/conf,release=0.1.36,update=True
        """
        execute(prepare_update_host,
                requirements_list=requirements_list,
                bootstrap_path=bootstrap_path,
                release=release,
                bootstrap_branch=bootstrap_branch)
