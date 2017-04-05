import uuid
import os

from datetime import datetime
from pathlib import PurePath

from fabric.api import execute, task, env, put, sudo, cd, run, lcd, local
from fabric.contrib.files import sed, exists
from fabric.decorators import roles
from fabric.utils import abort

from bcpp_fabric.new.fabfile import (
    prepare_deploy, deploy, update_fabric_env,
    update_fabric_env_device_ids,
    update_fabric_env_key_volumes,
    mount_dmg, prepare_deployment_host)
from bcpp_fabric.new.fabfile.utils import (
    get_hosts, get_device_ids, update_env_secrets,
    create_venv, pip_install_from_cache, get_archive_name,
    bootstrap_env, install_gpg, test_connection, gpg)
from bcpp_fabric.new.fabfile.repositories import get_repo_name
from bcpp_fabric.new.fabfile.mysql import install_mysql
from bcpp_fabric.new.fabfile.nginx import install_nginx

from .patterns import hostname_pattern
from .roledefs import roledefs

CONFIG_FILENAME = 'bcpp.conf'
DOWNLOADS_DIR = '~/Downloads'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'etc')
FABRIC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'conf', 'fabric.conf')

env.log_folder = os.path.expanduser('~/fabric/{}'.format(
    datetime.now().strftime('%Y%m%d%H%M%S')))
os.makedirs(env.log_folder)
print('log_folder', env.log_folder)
update_env_secrets(path=ETC_CONFIG_PATH)
env.roledefs = roledefs
env.hosts, env.passwords = get_hosts(
    path=ETC_CONFIG_PATH, gpg_filename='hosts.conf.gpg')
env.hostname_pattern = hostname_pattern
env.device_ids = get_device_ids()

with open(os.path.join(env.log_folder, 'hosts.txt'), 'a') as f:
    f.write('{}\n'.format(',\n'.join([h for h in env.hosts])))

# env.skip_bad_hosts = True
env.session = uuid.uuid4().hex


@task
def deployment_host(bootstrap_path=None, release=None, skip_clone=None, use_branch=None):
    execute(prepare_deployment_host,
            bootstrap_path=bootstrap_path,
            release=release,
            skip_clone=skip_clone,
            use_branch=use_branch)


@task
def deploy_centralserver():
    with lcd(BASE_DIR):
        result = local('git status')
        results = result.split('\n')
        if results[0] != 'On branch master':
            abort(results[0])


@task
def deploy_communityserver():
    pass


@task
def mysql():
    pass


@task
def deploy_client(bootstrap_path=None, release=None, map_area=None, user=None):
    """Deploy clients from the deployment host.

    Assumes you have already prepared the deployment host
    """
    bootstrap_env(path=bootstrap_path, filename='bootstrap_client.conf')
    if not release:
        abort('Specify the release')
    if not map_area:
        abort('Specify the map_area')
    env.project_release = release
    env.map_area = map_area
    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)
    run('mkdir -p {path}'.format(path=str(PurePath(env.deployment_root).parent)))
    path = str(PurePath(env.deployment_root).parent)
    archive_name = get_archive_name()
    put(local_path=os.path.join(path, archive_name), remote_path=path)
    with cd(path):
        run('tar -xjf {archive_name}'.format(archive_name=archive_name))
    update_fabric_env()
    install_mysql()
    install_nginx()
    create_venv(name=env.venv_name,
                venv_dir=env.venv_dir,
                create_env=True,
                update_requirements=False)
    pip_install_from_cache()


# @task
# def deploy_client2(config_path=None, user=None, map_area=None):
#     env.map_area = map_area
#     update_fabric_env(fabric_config_path=FABRIC_CONFIG_PATH)
#     update_fabric_env_device_ids()
#     update_fabric_env_hosts()
#     update_fabric_env_key_volumes()
#     execute(prepare_deploy, config_path=FABRIC_CONFIG_PATH, user=user)
#     execute(put_project_conf)
#     execute(update_project_conf, map_area=map_area)
#     execute(update_settings)
#     execute(deploy, config_path=FABRIC_CONFIG_PATH,
#             user=user, update_environment=False)
#     env.prompts = {'Enter disk image passphrase:': env.key_volume_password}
#     execute(mount_dmg, dmg_filename=env.dmg_filename,
#             dmg_path=env.dmg_path)


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
