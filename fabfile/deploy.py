import uuid
import os

from datetime import datetime
from pathlib import PurePath

from fabric.api import execute, task, env, put, sudo, cd, run, lcd, local, warn, prefix
from fabric.colors import yellow
from fabric.contrib.files import sed, exists
from fabric.utils import abort
from fabric.contrib import django

from bcpp_fabric.new.fabfile import (
    prepare_deploy, deploy, update_fabric_env,
    mount_dmg, prepare_deployment_host, pip_install_from_cache,
    pip_install_requirements_from_cache, make_virtualenv,
    install_virtualenv, create_venv,
    install_mysql, install_protocol_database)
from bcpp_fabric.new.fabfile.env import update_env_secrets
from bcpp_fabric.new.fabfile.utils import (
    get_hosts, get_device_ids, get_archive_name,
    bootstrap_env, install_gpg, test_connection, gpg, ssh_copy_id,
    install_python3)
from bcpp_fabric.new.fabfile.repositories import get_repo_name
from bcpp_fabric.new.fabfile.nginx import install_nginx

from .patterns import hostname_pattern
from .roledefs import roledefs
from bcpp_fabric.new.fabfile.gunicorn.tasks import install_gunicorn
from fabric.contrib.project import rsync_project
from bcpp_fabric.new.fabfile.brew.tasks import update_brew_cache


django.settings_module('bcpp.settings')

CONFIG_FILENAME = 'bcpp.conf'
DOWNLOADS_DIR = '~/Downloads'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ETC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'etc')
FABRIC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'conf', 'fabric.conf')

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
env.log_folder = os.path.expanduser('~/fabric/{}'.format(timestamp))
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


@task
def deployment_host(bootstrap_path=None, release=None, skip_clone=None, skip_pip_download=None,
                    use_branch=None, bootstrap_branch=None):
    """
    Example:
        fab -H localhost deploy.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,use_branch=True,bootstrap_branch=develop,skip_pip_download=True,skip_clone=True
    """
    execute(prepare_deployment_host,
            bootstrap_path=bootstrap_path,
            release=release,
            skip_clone=skip_clone,
            skip_pip_download=skip_pip_download,
            use_branch=use_branch,
            bootstrap_branch=bootstrap_branch)


@task
def deploy_centralserver(local_branch=None):
    pass


@task
def deploy_communityserver():
    pass


@task
def mysql():
    pass


@task
def deploy_client(bootstrap_path=None, release=None, map_area=None, user=None,
                  bootstrap_branch=None, database=None):
    """Deploy clients from the deployment host.

    Assumes you have already prepared the deployment host

    Will use conf files on deployment

    Example:
        fab -H 10.113.201.56 deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,bootstrap_branch=develop,map_area=lentsweletau --user=django    
        fab -P -R testhosts deploy_client:release=develop,bootstrap_branch=develop,map_area=lentsweletau,bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/ --user=django    

    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)
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

    rsync_deployment_root()

    update_brew_cache()

    put_bash_profile()
#     if database:
#         run('scp -C {database} {path}'.format(
#             database=database,
#             path=str(PurePath(env.deployment_root).parent)))
#     else:
#         warn('No database specified')
    update_fabric_env()

    # archve existing source
    if exists(os.path.join(env.remote_source_root, env.project_repo_name)):
        with cd(env.remote_source_root):
            run('tar -cjf {project_appname}_{timestamp}.tar.gz {project_appname}'.format(
                project_appname=env.project_appname,
                timestamp=timestamp))
    else:
        run('mkdir -p {remote_source_root}'.format(
            remote_source_root=env.remote_source_root), warn_only=True)

    remote_media = os.path.join(env.remote_source_root, 'media')
    if exists(remote_media):
        run('cp -R {old_remote_media}/ {new_remote_media}'.format(
            old_remote_media=remote_media,
            new_remote_media=env.media_root))
    remote_static = os.path.join(
        env.remote_source_root, env.project_repo_name, 'static')
    if exists(remote_static):
        run('cp -R {remote_static}/ {static_root}'.format(
            remote_static=remote_static,
            static_root=env.static_root))
    run('rm -rf {remote_source_root}'.format(
        remote_source_root=env.remote_source_root))

    # copy repo from deployment to source
    destination = env.remote_source_root
    if not exists(destination):
        run('mkdir -p {destination}'.format(destination=destination))
    run('cp -R {source} {destination}/'.format(
        source=os.path.join(env.deployment_root, env.project_appname),
        destination=destination))

    with cd(os.path.join(env.project_repo_root)):
        run('git checkout master')

    # make static and media
    if not exists(env.static_root):
        run('mkdir {static_root}'.format(
            static_root=env.static_root), warn_only=True)
    if not exists(env.media_root):
        run('mkdir {media_root}'.format(
            media_root=env.media_root), warn_only=True)

    install_mysql()
    # mysql copy archive, backup, drop create, timezone, restore

    install_python3()
    # install_gunicorn()

    install_nginx(skip_bootstrap=True)

    create_venv()

    # copy bcpp.conf into etc/{project_app_name}/
    put_project_conf()
    update_bcpp_conf()
    # crypto_keys DMG into etc/{project_app_name}/
    put(os.path.expanduser(os.path.join(env.fabric_config_root, 'etc', env.dmg_filename)),
        '/etc/{project_appname}/'.format(
        project_appname=env.project_appname), use_sudo=True)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        result = run(
            'git diff --name-status master..{release}'.format(release=release))
        if result:
            warn('master is not at {release}'.format(release=release))

    update_settings()
    # scripts (e.g. mount dmg)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        with prefix('workon {venv_name}'.format(venv_name=env.venv_name)):
            run('python manage.py collectstatic')
            run('python manage.py collectstatic_js_reverse')

    install_protocol_database()
    # start gunicorn / nginx


def rsync_deployment_root():
    remote_path = str(PurePath(env.deployment_root).parent)
    if not exists(remote_path):
        run('mkdir -p {path}'.format(path=remote_path))
    local_path = '{}'.format(os.path.expanduser(env.deployment_root))
    rsync_project(local_dir=local_path, remote_dir=remote_path)


def update_settings():
    with cd(os.path.join(env.remote_source_root, env.project_repo_name, env.project_appname)):
        sed('settings.py', 'DEBUG \=.*', 'DEBUG \= False')
        sed('settings.py', 'ANONYMOUS_ENABLED \=.*',
            'ANONYMOUS_ENABLED \= False')


def put_project_conf(project_conf=None, map_area=None):
    """Copies the projects <appname>.conf file to remote etc_dir.
    """
    project_conf = project_conf or env.project_conf
    local_copy = os.path.expanduser(os.path.join(
        env.fabric_config_root, 'conf', project_conf))
    remote_copy = os.path.join(env.etc_dir, project_conf)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))
    put(local_copy, remote_copy, use_sudo=True)
    sed(remote_copy, 'device_id \=.*',
        'device_id \= {}'.format(env.device_ids.get(env.host)),
        use_sudo=True)
    sed(remote_copy, 'role \=.*',
        'role \= {}'.format('env.device_roles.get(env.host)'),
        use_sudo=True)
    sed(remote_copy, 'key_path \=.*',
        'key_path \= {}'.format(env.key_path),
        use_sudo=True)
    sed(remote_copy, 'secret_key =.*',
        'secret_key \= {}'.format(env.secret_key),
        use_sudo=True)
    sed(remote_copy, 'database \=.*',
        'database \= {}'.format(env.dbname),
        use_sudo=True)
    sed(remote_copy, 'password \=.*',
        'password \= {}'.format(env.dbpasswd),
        use_sudo=True)


@task
def update_bcpp_conf(project_conf=None, map_area=None):
    """Updates the bcpp.conf file on the remote host.
    """
    project_conf = project_conf or env.project_conf
    remote_copy = os.path.join(env.etc_dir, project_conf)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))
    sed(remote_copy, 'map_area \=.*',
        'map_area \= {}'.format(env.map_area or ''),
        use_sudo=True)


def put_bash_profile():
    """Copies the bash_profile.
    """
    local_copy = os.path.expanduser(os.path.join(
        env.fabric_config_root, 'conf', 'bash_profile'))
    remote_copy = '~/.bash_profile'
    put(local_copy, remote_copy)
    result = run('source ~/.bash_profile')
    if result:
        abort(result)
