import uuid
import os

from datetime import datetime
from pathlib import PurePath

from fabric.api import execute, task, env, put, sudo, cd, run, lcd, local, warn, prefix
from fabric.colors import yellow, blue
from fabric.contrib.files import sed, exists
from fabric.contrib.project import rsync_project
from fabric.utils import abort
from fabric.contrib import django

from bcpp_fabric.new.fabfile import (
    update_fabric_env,
    mount_dmg, prepare_deployment_host, pip_install_from_cache,
    pip_install_requirements_from_cache, make_virtualenv,
    install_virtualenv, create_venv,
    install_mysql, install_protocol_database, prompts)
from bcpp_fabric.new.fabfile.brew import update_brew_task, update_brew_cache
from bcpp_fabric.new.fabfile.conf import put_project_conf
from bcpp_fabric.new.fabfile.environment import update_env_secrets
from bcpp_fabric.new.fabfile.utils import (
    get_hosts, get_device_ids, update_settings, rsync_deployment_root,
    bootstrap_env, put_bash_profile, test_connection, ssh_copy_id,
    install_python3, test_connection2, touch_host)
from bcpp_fabric.new.fabfile.repositories import get_repo_name
from bcpp_fabric.new.fabfile.nginx import install_nginx, install_nginx_task
from bcpp_fabric.new.fabfile.gunicorn import install_gunicorn_task, install_gunicorn

from .patterns import hostname_pattern
from .roledefs import roledefs


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
env.prompts = prompts

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
                  bootstrap_branch=None, database=None, skip_db_restore=None,
                  skip_venv=None, device_role=None, device_id=None):
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
    env.device_role = device_role or env.device_role
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

    update_fabric_env()

    update_brew_cache(no_auto_update=True)

    put_bash_profile()

    if not exists(os.path.join(env.remote_source_root, env.project_repo_name)):
        run('mkdir -p {remote_source_root}'.format(
            remote_source_root=env.remote_source_root), warn_only=True)

    # move media folder out of project repo
    move_media_folder()
    sudo('rm -rf {remote_source_root}'.format(
        remote_source_root=env.remote_source_root))

    # copy repo from deployment to source
    destination = env.remote_source_root
    if not exists(destination):
        run('mkdir -p {destination}'.format(destination=destination))
    run('rsync -pthrvz --delete {source} {destination}'.format(
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

    install_python3()

    if not skip_venv:
        create_venv()

    # copy bcpp.conf into etc/{project_app_name}/
    env.device_id = device_id
    put_project_conf()
    update_bcpp_conf()

    if env.log_root and exists(env.log_root):
        sudo('rm -rf {log_root}'.format(log_root=env.log_root), warn_only=True)
    run('mkdir -p {log_root}'.format(log_root=env.log_root))
    install_nginx(skip_bootstrap=True)
    install_gunicorn()

    # crypto_keys DMG into etc/{project_app_name}/
    put(os.path.expanduser(os.path.join(env.fabric_config_root, 'etc', env.dmg_filename)),
        env.etc_dir,
        use_sudo=True)

    # mount dmg
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        run('git checkout master')
        result = run(
            'git diff --name-status master..{release}'.format(release=release))
        if result:
            warn('master is not at {release}'.format(release=release))

    update_settings()

    if not skip_db_restore:
        install_protocol_database()

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        with prefix('workon {venv_name}'.format(venv_name=env.venv_name)):
            run('python manage.py collectstatic')
            run('python manage.py collectstatic_js_reverse')

    sudo('launchctl unload -F /Library/LaunchDaemons/nginx.plist', warn_only=True)
    sudo('nginx -s stop', warn_only=True)
    run('launchctl unload -F /Library/LaunchDaemons/gunicorn.plist', warn_only=True)
#     sudo('ps aux | grep gunicorn | awk \'{print $2}\' | xargs kill -9',
#          warn_only=True)
    sudo('launchctl load -F /Library/LaunchDaemons/nginx.plist')
    run('launchctl load -F /Library/LaunchDaemons/gunicorn.plist')
    run('curl http://localhost')


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


@task
def relaunch_web():
    sudo('launchctl unload -F /Library/LaunchDaemons/nginx.plist', warn_only=True)
    sudo('nginx -s stop', warn_only=True)
    run('launchctl unload -F /Library/LaunchDaemons/gunicorn.plist', warn_only=True)
    sudo('ps auxww | grep gunicorn | awk \'{print $2}\' | xargs kill -9',
         warn_only=True)
    sudo('launchctl load -F /Library/LaunchDaemons/nginx.plist')
    run('launchctl load -F /Library/LaunchDaemons/gunicorn.plist')


@task
def install_protocol_database_task(bootstrap_path=None, bootstrap_branch=None, db_archive_name=None, skip_backup=None):
    """Overwrites the client DB.
    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)

    rsync_deployment_root()

    update_fabric_env()

    install_protocol_database(
        db_archive_name=db_archive_name, skip_backup=skip_backup)


@task
def validate(release=None, pull=None):
    result = run('workon bcpp', warn_only=True)
    if result:
        warn(yellow(f'{env.host}: {result}'))
    else:
        result = run('workon bcpp && python --version', warn_only=True)
        if result != 'Python 3.6.1':
            warn(yellow(f'{env.host}: {result}'))
        else:
            with cd('~/source/bcpp'):
                result = run('git tag')
                if release not in result:
                    result = run('git describe --abbrev=0 --tags')
                    warn(yellow(f'{env.host}: bcpp tag not found. Got {result}'))
                    if pull:
                        run('git pull')
            result = run('curl http://localhost')
            if 'Bad Gateway' in result:
                warn(yellow(f'{env.host}: bad gateway'))
            else:
                result = run(
                    'curl http://localhost/static/bcpp/label_templates/aliquot.lbl')
                if '404 Not Found' in result:
                    warn(yellow(f'{env.host}: 404 Not Found'))
                else:
                    if not exists('~/media/edc_map') or not exists('~/media/transactions'):
                        warn(yellow(f'{env.host}: Media folder not ready'))
                    else:
                        warn(blue(f'{env.host}: OK'))


@task
def move_media_folder_task(bootstrap_path=None, bootstrap_branch=None, use_local_fabric_conf=True):
    """Moves media folder out of the source repo.
    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)

    update_fabric_env(use_local_fabric_conf=use_local_fabric_conf)
    move_media_folder()


def move_media_folder():
    """Moves media folder out of the source repo.
    """
    old_remote_media = os.path.join(
        env.remote_source_root, env.project_repo_name, 'media')
    if exists(old_remote_media):
        run(f'rsync -pthrvz --remove-source-files {old_remote_media} ~/', warn_only=True)


@task
def fetch_map_images_task():
    with cd('~/source/bcpp'):
        with prefix('source ~/.venvs/bcpp/bin/activate'):
            run('python manage.py fetch_map_images plot.plot 10')
