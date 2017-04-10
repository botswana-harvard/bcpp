import os

from fabric.api import task, run

from bcpp_fabric.new.fabfile.environment import (
    bootstrap_env, update_fabric_env)

from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project


@task
def restore_media_folder(bootstrap_path=None, bootstrap_branch=None, use_local_fabric_conf=True):
    """Restores media/edc_map from the external backup
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
