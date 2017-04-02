import os

from fabric.api import execute, task, env, put, sudo, cd
from fabric.contrib.files import sed, exists

from bcpp_fabric.new.fabfile import (
    prepare_deploy, deploy, update_fabric_env,
    update_fabric_env_device_ids, update_fabric_env_hosts, update_fabric_env_key_volumes,
    mount_dmg, update_fabric_env_skip_prompts, prepare_local_for_deploy)
from bcpp_fabric.new.fabfile.constants import MACOSX

CONFIG_FILENAME = 'bcpp.conf'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRIC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'fabric.conf')


@task
def deploy_local():
    execute(prepare_local_for_deploy,
            project_repo_url='https://github.com/botswana-harvard/bcpp.git',
            tag='0.1.8',
            target_os=MACOSX)


@task
def deploy_centralserver():
    pass


@task
def deploy_communityserver():
    pass


@task
def mysql():
    pass


@task()
def deploy_client(config_path=None, user=None, map_area=None):
    if not map_area:
        map_area = input('Enter the map_area:')
    env.map_area = map_area
    update_fabric_env(fabric_config_path=FABRIC_CONFIG_PATH)
    update_fabric_env_device_ids()
    update_fabric_env_hosts()
    update_fabric_env_key_volumes()
    update_fabric_env_skip_prompts()
    execute(prepare_deploy, config_path=FABRIC_CONFIG_PATH, user=user)
    execute(put_project_conf)
    execute(update_project_conf, map_area=map_area)
    execute(update_settings)
    execute(deploy, config_path=FABRIC_CONFIG_PATH,
            user=user, update_environment=False)
    execute(put_key_volume)
    env.prompts = {'Enter disk image passphrase:': env.key_volume_password}
    execute(mount_dmg, dmg_filename=env.dmg_filename,
            dmg_path=env.dmg_path)


@task
def update_settings():
    with cd(os.path.join(env.remote_source_root, env.project_appname, env.project_appname)):
        sed('settings.py', 'DEBUG \=.*', 'DEBUG \= False')
        sed('settings.py', 'ANONYMOUS_ENABLED \=.*',
            'ANONYMOUS_ENABLED \= False')


@task
def put_project_conf(config_filename=None, map_area=None):
    """Copies the projects <appname>.conf file to remote etc_dir.
    """
    config_filename = config_filename or CONFIG_FILENAME
    local_copy = os.path.join(os.path.expanduser(
        env.deployment_root), config_filename)
    remote_copy = os.path.join(env.etc_dir, config_filename)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))
    put(local_copy, remote_copy, use_sudo=True)
    sed(remote_copy, 'device_id \=.*',
        'device_id \= {}'.format(env.device_ids.get(env.host)),
        use_sudo=True)
    sed(remote_copy, 'role \=.*',
        'role \= {}'.format(env.device_roles.get(env.host)),
        use_sudo=True)
    sed(remote_copy, 'key_path \=.*',
        'key_path \= {}'.format(env.key_path),
        use_sudo=True)


@task
def update_project_conf(config_filename=None, map_area=None):
    """Updates the bcpp.conf file on the remote host.
    """
    config_filename = config_filename or CONFIG_FILENAME
    local_copy = os.path.join(os.path.expanduser(
        env.deployment_root), config_filename)
    remote_copy = os.path.join(env.etc_dir, config_filename)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))
    put(local_copy, remote_copy, use_sudo=True)
    sed(remote_copy, 'map_area \=.*',
        'map_area \= {}'.format(env.map_area or ''),
        use_sudo=True)


@task
def put_key_volume(config_filename=None, map_area=None):
    """Copies the key volume file to remote etc_dir.
    """
    config_filename = config_filename or CONFIG_FILENAME
    local_copy = os.path.join(os.path.expanduser(
        env.deployment_root), env.dmg_filename)
    remote_copy = os.path.join(env.etc_dir, env.dmg_filename)
    put(local_copy, remote_copy, use_sudo=True)
