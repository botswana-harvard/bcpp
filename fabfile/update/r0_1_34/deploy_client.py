import os

from fabric.api import cd, run, env, task, abort

from edc_fabric.fabfile.utils import launch_webserver, update_settings, \
    rsync_deployment_root
from edc_fabric.fabfile.pip.tasks import get_pip_list
from edc_fabric.fabfile.mysql.tasks import install_protocol_database, \
    put_my_cnf, put_mysql_conf
from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.gunicorn.tasks import install_gunicorn
from edc_fabric.fabfile.virtualenv.tasks import create_venv

from fabfile.prepare_env import prepare_env
from fabfile.utils import update_bcpp_conf


@task
def r0134(bootstrap_filename=None, skip_update_project_repo=None,
          skip_venv=None, map_area=None, **kwargs):
    """Release 0.1.34.
    """
    release = '0.1.34'
    bootstrap_filename = bootstrap_filename or 'bootstrap_client.conf'
    if not map_area:
        abort('Specify the map_area')

    prepare_env(release=release,
                bootstrap_filename=bootstrap_filename,
                map_area=map_area,
                **kwargs)

    rsync_deployment_root()

    if not skip_update_project_repo:
        print('rsync -pthrvz --delete {source} {destination}'.format(
            source=os.path.join(env.deployment_root, env.project_appname),
            destination=env.remote_source_root))
        run('rsync -pthrvz --delete {source} {destination}'.format(
            source=os.path.join(env.deployment_root, env.project_appname),
            destination=env.remote_source_root))

    with cd(os.path.join(env.project_repo_root)):
        run('git checkout master')

    if not skip_venv:
        create_venv()
    install_gunicorn()

    # copy bcpp.conf into etc/{project_app_name}/
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)
    put_mysql_conf()
    put_my_cnf()
    put_project_conf()
    update_bcpp_conf()
    update_settings()

    install_protocol_database(skip_backup=True)

    get_pip_list()

    launch_webserver()
