import os
from pathlib import PurePath

from fabric.api import execute, task, env, put, sudo, cd, run, lcd
from fabric.contrib.files import sed, exists
from fabric.decorators import roles

from bcpp_fabric.new.fabfile import (
    prepare_deploy, deploy, update_fabric_env,
    update_fabric_env_device_ids, update_fabric_env_hosts, update_fabric_env_key_volumes,
    mount_dmg, prepare_deployment_host)
from bcpp_fabric.new.fabfile.utils import (
    get_hosts, get_device_ids,
    create_venv, install_venv, download_pip_archives, get_archive_name)

from .patterns import hostname_pattern
from .roledefs import roledefs
from bcpp_fabric.new.fabfile.deployment_host.deploy import update_env_secrets
from fabric.utils import abort

CONFIG_FILENAME = 'bcpp.conf'
DOWNLOADS_DIR = '~/Downloads'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'etc')
FABRIC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'conf', 'fabric.conf')

# env.hosts = get_hosts(path=HOST_CONFIG_PATH, gpg_filename='hosts.conf.gpg')
env.roledefs = roledefs
env.hostname_pattern = hostname_pattern
# env.device_ids = get_device_ids()


@task
@roles('deployment_hosts')
def deployment_host(bootstrap_path=None, release=None, skip_clone=None, use_branch=None):
    execute(prepare_deployment_host,
            bootstrap_path=bootstrap_path,
            release=release,
            skip_clone=skip_clone,
            use_branch=use_branch)
    create_venv(name=env.project_appname,
                venv_dir=os.path.join(env.deployment_root, 'venv'),
                create_env=True,
                update_requirements=False)
    with cd(str(PurePath(env.deployment_root).parent)):
        path = PurePath(env.deployment_root).parts[-1:][0]
        archive_name = get_archive_name(
            deployment_root=env.deployment_root, release=release)
        run('tar -cjf {archive_name} {path}'.format(archive_name=archive_name, path=path))


@task
def deploy_centralserver():
    pass


@task
def deploy_communityserver():
    pass


@task
def mysql():
    pass


@task
def deploy_client(project_appname=None, deployment_root=None, release=None, map_area=None, user=None):
    if not project_appname:
        abort('Specify the project_appname (e.g. bcpp)')
    if not deployment_root:
        abort('Specify the deployment_root')
    if not release:
        abort('Specify the release')
    env.map_area = map_area
    env.deployment_root = deployment_root
    env.project_appname = project_appname
    path = str(PurePath(env.deployment_root).parent)
    run('mkdir -p {path}'.format(path=str(PurePath(env.deployment_root).parent)))
    path = str(PurePath(env.deployment_root).parent)
    archive_name = get_archive_name(
        deployment_root=deployment_root, release=release)
    put(local_path=os.path.join(path, archive_name), remote_path=path)
    with cd(path):
        run('tar -xjf {archive_name}'.format(archive_name=archive_name))
    install_venv(venv_name=project_appname)
    update_env_secrets()
    update_fabric_env()


@task
def deploy_client2(config_path=None, user=None, map_area=None):
    env.map_area = map_area
    update_fabric_env(fabric_config_path=FABRIC_CONFIG_PATH)
    update_fabric_env_device_ids()
    update_fabric_env_hosts()
    update_fabric_env_key_volumes()
    execute(prepare_deploy, config_path=FABRIC_CONFIG_PATH, user=user)
    execute(put_project_conf)
    execute(update_project_conf, map_area=map_area)
    execute(update_settings)
    execute(deploy, config_path=FABRIC_CONFIG_PATH,
            user=user, update_environment=False)
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
