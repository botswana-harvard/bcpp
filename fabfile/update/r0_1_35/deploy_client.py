import os

from fabric.api import cd, run, env, warn, task

from edc_fabric.fabfile.pip.tasks import pip_install_from_cache, pip_download
from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.mysql.tasks import install_protocol_database
from edc_fabric.fabfile.utils import rsync_deployment_root, update_settings,\
    launch_webserver

from fabfile.prepare_env import prepare_env


@task
def r0135(**kwargs):
    """Release 0.1.35.
    """

    release = '0.1.34'
    packages = ['git+https://github.com/botswana-harvard/bcpp-subject.git@master#egg=bcpp_subject',
                'git+https://github.com/botswana-harvard/plot.git@master#egg=plot']

    bootstrap_filename = 'bootstrap_client.conf'

    prepare_env(bootstrap_filename=bootstrap_filename, **kwargs)

    venv_name = env.venv_name

    rsync_deployment_root()

    venv_name = venv_name or env.venv_name
    # copy new pip tarballs to deployment root
    for package in packages:
        pip_download(package)

    with cd('/Users/django/source/bcpp'):
        run('git stash')
        run('git pull')
        run('git stash pop')

#     for package in packages:
    uninstall_package = package.split('=')[1]
    run('workon {venv_name} && pip3 uninstall {package_name}'.format(
        venv_name=venv_name,
        package_name=uninstall_package))
    pip_install_from_cache(package_name=package, venv_name=venv_name)

    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        run('git checkout master')
        result = run(
            'git diff --name-status master..{release}'.format(release=release))
        if result:
            warn('master is not at {release}'.format(release=release))

    update_settings()

    install_protocol_database()

    launch_webserver()
