import os

from datetime import datetime

from fabric.api import execute, task, env, put, sudo, cd, run, warn, prefix, lcd
from fabric.contrib.files import exists
from fabric.utils import abort
from fabric.contrib import django

from edc_device.constants import CENTRAL_SERVER

from edc_fabric.fabfile import (
    update_fabric_env,
    prepare_deployment_host, create_venv,
    install_mysql, install_protocol_database, prompts)
from edc_fabric.fabfile.brew import update_brew_cache
from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.constants import MACOSX, LINUX
from edc_fabric.fabfile.environment import update_env_secrets
from edc_fabric.fabfile.files import mount_dmg_locally, dismount_dmg_locally, mount_dmg
from edc_fabric.fabfile.gunicorn import install_gunicorn
from edc_fabric.fabfile.nginx import install_nginx
from edc_fabric.fabfile.python import install_python3
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import (
    get_hosts, get_device_ids, update_settings, rsync_deployment_root,
    bootstrap_env, put_bash_config, ssh_copy_id,
    test_connection2, move_media_folder, launch_webserver)
from edc_fabric.fabfile.virtualenv import activate_venv

from .patterns import hostname_pattern
from .roledefs import roledefs
from .utils import update_bcpp_conf

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

env.prompts.update({'Enter password: ': env.dbpasswd})

with open(os.path.join(env.log_folder, 'hosts.txt'), 'a') as f:
    f.write('{}\n'.format(',\n'.join([h for h in env.hosts])))

# env.skip_bad_hosts = True


@task
def deployment_host(bootstrap_path=None, release=None, skip_clone=None, skip_pip_download=None,
                    use_branch=None, bootstrap_branch=None):
    """
    Example:

        brew update && fab -H localhost deploy.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,use_branch=True,bootstrap_branch=develop,skip_pip_download=True,skip_clone=True

    """
    execute(prepare_deployment_host,
            bootstrap_path=bootstrap_path,
            release=release,
            skip_clone=skip_clone,
            skip_pip_download=skip_pip_download,
            use_branch=use_branch,
            bootstrap_branch=bootstrap_branch)


@task
def deploy_centralserver(**kwargs):
    """

        fab -H bhp066 deploy.deploy_centralserver:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.26,map_area=botswana --user=django

    """

    conf_filename = 'bootstrap_centralserver.conf'
    deploy(conf_filename=conf_filename, **kwargs)


@task
def deploy_nodeserver(**kwargs):
    conf_filename = 'bootstrap_nodeserver.conf'
    deploy(conf_filename=conf_filename, **kwargs)


@task
def deploy_client(**kwargs):
    """Deploy clients from the deployment host.

    Assumes you have already prepared the deployment host

    Will use conf files on deployment

    For example:

    Copy ssh keys:

        fab -P -R mmankgodi deploy.ssh_copy_id:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf,bootstrap_branch=develop --user=django

    Deploy:

        fab -H bcpp038 deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.24,map_area=mmankgodi --user=django

    - OR -

        fab -P -R mmankgodi deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.24,map_area=mmankgodi --user=django

    Once complete:

        fab -P -R mmankgodi deploy.validate:release=0.1.24 --user=django

    """
    conf_filename = 'bootstrap_client.conf'
    deploy(conf_filename=conf_filename, **kwargs)


def deploy(conf_filename=None, bootstrap_path=None, release=None, map_area=None, user=None,
           bootstrap_branch=None, skip_update_os=None, skip_db=None, skip_repo=None,
           skip_venv=None, skip_mysql=None, skip_python=None, skip_web=None,
           skip_collectstatic=None, skip_bash_config=None, work_online=None):
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

    rsync_deployment_root()

    update_fabric_env()

    if not skip_update_os:
        if env.target_os == MACOSX:
            update_brew_cache(no_auto_update=True)
        elif env.target_os == LINUX:
            sudo('apt-get update')

    if not skip_bash_config:
        put_bash_config()

    if not exists(os.path.join(env.remote_source_root, env.project_repo_name)):
        run('mkdir -p {remote_source_root}'.format(
            remote_source_root=env.remote_source_root), warn_only=True)

    if not skip_repo:
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

    if not skip_mysql:
        install_mysql()

    if not skip_python:
        install_python3()

    if not skip_venv:
        create_venv(work_online=work_online)

    # copy bcpp.conf into etc/{project_app_name}/
    put_project_conf()
    update_bcpp_conf()

    if not skip_web:
        if env.log_root and exists(env.log_root):
            sudo('rm -rf {log_root}'.format(log_root=env.log_root),
                 warn_only=True)
        run('mkdir -p {log_root}'.format(log_root=env.log_root))
        install_nginx(skip_bootstrap=True)
        install_gunicorn(work_online=work_online)

    # crypto_keys DMG into etc/{project_app_name}/
    put(os.path.expanduser(os.path.join(env.fabric_config_root, 'etc', env.dmg_filename)),
        env.etc_dir,
        use_sudo=True)

    # mount dmg
    if env.device_role == CENTRAL_SERVER:
        mount_dmg_locally(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                          dmg_passphrase=env.crypto_keys_passphrase)
        if not exists(env.key_path):
            sudo(f'mkdir -p {env.key_path}')
        with lcd(env.key_volume):
            put(local_path='user*',
                remote_path=f'{env.key_path}/', use_sudo=True)
        dismount_dmg_locally(volume_name=env.key_volume)
    else:
        mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                  dmg_passphrase=env.crypto_keys_passphrase)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        run('git checkout master')
        result = run(
            'git diff --name-status master..{release}'.format(release=release))
        if result:
            warn('master is not at {release}'.format(release=release))

    update_settings()

    if not skip_db:
        install_protocol_database()

    if not skip_collectstatic:
        with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
            with prefix(f'source {activate_venv()}'.format(venv_name=env.venv_name)):
                run('python manage.py collectstatic')
                run('python manage.py collectstatic_js_reverse')

    launch_webserver(work_online=work_online)
