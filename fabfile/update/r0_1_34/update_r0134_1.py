from fabric.api import env, task, run, cd
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from fabric.utils import abort

from edc_fabric.fabfile.deployment_host import prepare_deployment_dir
from edc_fabric.fabfile.environment import bootstrap_env
from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.pip import pip_install_from_cache, pip_download
from edc_fabric.fabfile.utils import (
    launch_webserver, rsync_deployment_root)

from ...prepare_env import prepare_env


@task
def deployment_host(bootstrap_path=None, release=None, skip_clone=True, deployment_pip_dir=None,
                    map_area=None, bootstrap_filename=None, bootstrap_branch=None, **kwargs):
    """
    Example:

        brew update && fab -H localhost update.deployment_host:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=develop,use_branch=True,bootstrap_branch=develop,skip_pip_download=True,skip_clone=True

    """
    release = '0.1.34'
    packages = ['git+https://github.com/botswana-harvard/bcpp-subject.git@master#egg=bcpp_subject',
                'git+https://github.com/botswana-harvard/plot.git@master#egg=plot']

#     bootstrap_filename = bootstrap_filename or 'bootstrap_client.conf'
    if not map_area:
        abort('Specify the map_area')

    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap.conf',
        bootstrap_branch=bootstrap_branch)
#
    prepare_env(release=release,
                bootstrap_filename=bootstrap_filename,
                map_area=map_area,
                **kwargs)

    prepare_deployment_dir()

    if not exists(env.deployment_pip_dir):
        run('mkdir -p {deployment_pip_dir}'.format(
            deployment_pip_dir=env.deployment_pip_dir))

    with cd(env.deployment_root):
        pip_download('pip')
        pip_download('setuptools')
        pip_download('wheel')
        for package in packages:
            run('pip3 download {package}'.format(
                package=package), warn_only=True)


def deploy_client(skip_db=None, bootstrap_filename=None, venv_name=None, map_area=None, **kwargs):

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


@task
def launch_webserver_bcpp(**kwargs):
    prepare_env(**kwargs)
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)
    launch_webserver()
