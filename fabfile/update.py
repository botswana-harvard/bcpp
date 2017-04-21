import os

from fabric.api import abort, env

from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.repositories import get_repo_name


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

    task_callable()
