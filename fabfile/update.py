import os

from fabric.api import abort, env, task, run, cd

from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.pip import pip_install_from_cache
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import launch_webserver

from .utils import update_bcpp_conf


def update_host(conf_filename=None, bootstrap_path=None, release=None,
                map_area=None, bootstrap_branch=None, work_online=None,
                task_callable=None):
    bootstrap_env(
        path=bootstrap_path,
        filename=conf_filename,
        bootstrap_branch=bootstrap_branch)
    if not release:
        abort('Specify the release')
    if not map_area:
        abort('Specify the map_area')
    print(env.target_os)
    env.project_release = release
    env.map_area = map_area
    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)
    update_fabric_env()


@task
def update_host_task(**kwargs):

    update_host()

    with cd(os.path.join(env.project_repo_root)):
        run('git checkout master')
        run('git pull')

    put_project_conf()
    update_bcpp_conf()

    package_names = ['bcpp_subject', 'member', 'household', 'plot']
    for package_name in package_names:
        pip_install_from_cache(package_name=package_name,
                               venv_name=env.venv_name)

    launch_webserver()
