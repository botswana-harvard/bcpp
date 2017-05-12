from fabric.api import env, task, run, cd
from fabric.context_managers import prefix
from fabric.utils import abort

from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.pip import pip_install_from_cache, pip_download
from edc_fabric.fabfile.utils import (
    launch_webserver, rsync_deployment_root)

from ...prepare_env import prepare_env


@task
def r01341(skip_db=None, bootstrap_filename=None, venv_name=None, map_area=None, **kwargs):
    """Release 0.1.34.1
    """

    release = '0.1.34'
    packages = ['git+https://github.com/botswana-harvard/bcpp-subject.git@master#egg=bcpp_subject',
                'git+https://github.com/botswana-harvard/plot.git@master#egg=plot']
    bootstrap_filename = bootstrap_filename or 'bootstrap_client.conf'

    if not map_area:
        abort('Specify the map_area')

    prepare_env(release=release,
                bootstrap_filename=bootstrap_filename,
                map_area=map_area,
                **kwargs)

    venv_name = venv_name or env.venv_name

    rsync_deployment_root()

    # copy new pip tarballs to deployment root
    for package in packages:
        pip_download(package)

    for package in packages:
        uninstall_package = package.split('=')[1]
        run('workon {venv_name} && pip3 uninstall {package_name}'.format(
            venv_name=venv_name,
            package_name=uninstall_package))
        pip_install_from_cache(package_name=package, venv_name=venv_name)

    with cd('/Users/django/source/bcpp'):
        with prefix('source /Users/django/.venvs/bcpp/bin/activate'):
            run('python manage.py update_anonymous_sectioning')

    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)

    launch_webserver()


def launch_webserver_bcpp(**kwargs):
    prepare_env(**kwargs)
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)
    launch_webserver()
