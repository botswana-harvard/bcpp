import os

from fabric.api import task, run

from fabric.api import warn, cd, env
from fabric.colors import yellow, blue
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project

from bcpp_fabric.new.fabfile.utils import rsync_deployment_root
from bcpp_fabric.new.fabfile.environment import (
    bootstrap_env, update_fabric_env)
from bcpp_fabric.new.fabfile.mysql import install_protocol_database


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
def restore_media_folder(bootstrap_path=None, bootstrap_branch=None, use_local_fabric_conf=True):
    """Restores media/edc_map from the external backup

    For example:

        fab -P -R mmankgodi utils.restore_media_folder:bootstrap_path=/Users/django/source/bcpp/fabfile/conf/,bootstrap_branch=develop,use_local_fabric_conf=True --user=django
    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)

    update_fabric_env(use_local_fabric_conf=use_local_fabric_conf)

    local_dir = '/Volumes/BONTSI/Village\ Maps/mmankgodi\ maps/media/edc_map'

    remote_dir = os.path.join('~/media/edc_map')

    if exists(remote_dir):
        run(f'rm -rf {remote_dir}', warn_only=True)
    run(f'mkdir -p {remote_dir}', warn_only=True)

    rsync_project(local_dir=local_dir, remote_dir=remote_dir)


@task
def install_protocol_database_task(bootstrap_path=None, bootstrap_branch=None,
                                   db_archive_name=None, skip_backup=None):
    """Overwrites the client DB.

    For example:

        fab -P -R lentsweletau deploy.install_protocol_database_task:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,bootstrap_branch=develo,db_archive_name=edc_deployment_201704092123.sql

    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)

    rsync_deployment_root()

    update_fabric_env()

    install_protocol_database(
        db_archive_name=db_archive_name, skip_backup=skip_backup)
