import os

from fabric.api import env, task, run, cd, get
from fabric.colors import red
from fabric.context_managers import lcd
from fabric.contrib.project import rsync_project
from fabric.operations import local
from fabric.utils import warn, abort

from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.gunicorn.tasks import install_gunicorn
from edc_fabric.fabfile.mysql import put_mysql_conf, put_my_cnf
from edc_fabric.fabfile.mysql.tasks import install_protocol_database
from edc_fabric.fabfile.pip import get_pip_list, pip_install_from_cache, pip_download
from edc_fabric.fabfile.pip.tasks import get_required_package_names
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import launch_webserver, update_settings, rsync_deployment_root
from edc_fabric.fabfile.virtualenv import create_venv

from .utils import update_bcpp_conf


def prepare_env(bootstrap_filename=None, bootstrap_path=None, release=None,
                map_area=None, bootstrap_branch=None, work_online=None,
                task_callable=None):
    bootstrap_env(
        path=bootstrap_path,
        filename=bootstrap_filename,
        bootstrap_branch=bootstrap_branch)
    env.project_release = release
    env.map_area = map_area
    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)
    update_fabric_env(use_local_fabric_conf=True)


@task
def query_tx_task(**kwargs):
    """Check for any host with pending transactions.

    fab -P -R mmankgodi update.query_tx_task:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    # run('brew services restart mysql', quiet=True)
    run('mysql -uroot -p edc -Bse \'select  count(*) '
        'from edc_sync_outgoingtransaction where is_consumed_server=0;\' > /tmp/stats1.txt')
    result = run('cat /tmp/stats1.txt')
    if result != '0':
        warn(red(f'{env.host}: pending {result}'))

    run(
        'mysql -uroot -p edc -Bse \'select count(*) '
        'from edc_sync_files_history '
        'where sent=0;\' > /tmp/stats2.txt')
    result = run('cat /tmp/stats2.txt')
    if result != '0':
        warn(red(f'{env.host}: unsent {result}'))


@task
def update_temp_task(map_area=None, bootstrap_filename=None, **kwargs):
    release = '0.1.34'
    if not map_area:
        abort('Specify the map_area')
    bootstrap_filename = bootstrap_filename or 'bootstrap_client.conf'
    prepare_env(release=release,
                bootstrap_filename=bootstrap_filename,
                map_area=map_area,
                **kwargs)
    run(f'rm ~/deployment/bcpp/database/{release}/{map_area}/edc_mmathethe_deployment_201704260014.sql', warn_only=True)
    local_path = os.path.expanduser(
        f'~/deployment/{release}/{map_area}/edc_mmathethe_deployment_201704260454.sql')
    remote_path = f'~/deployment/bcpp/database/{release}/{map_area}/edc_mmathethe_deployment_201704260454.sql'
    rsync_project(local_dir=local_path, remote_dir=remote_path)
    install_protocol_database(skip_backup=True)
    launch_webserver()


@task
def update_r0134_task(bootstrap_filename=None, skip_update_project_repo=None, skip_venv=None, map_area=None, **kwargs):

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

#     with cd(os.path.join(env.project_repo_root)):
#         run('git checkout master')
#         run('python manage.py makemigrations')
#         run('python manage.py makemigrations bcpp bcpp_subject members household plot')


@task
def get_pip_list_task(**kwargs):
    prepare_env(**kwargs)
    get_pip_list()
    result = run(
        'mysql -u root -pcc3721b edc -Bse \'select prev_batch_id from edc_sync_incomingtransaction LIMIT 1;\'')
    if 'ERROR' in result:
        warn(f'{env.host}: bad DB')


@task
def validate_db_task(**kwargs):
    prepare_env(**kwargs)
    result = run(
        'mysql -u root -pcc3721b edc -Bse \'select prev_batch_id from edc_sync_incomingtransaction LIMIT 1;\'')
    if 'ERROR' in result:
        warn(f'{env.host}: bad DB')


@task
def query_consent_task(**kwargs):
    """Query remote host subject consent table and download the result as a text file.
    """
    prepare_env(**kwargs)
    local_path = os.path.expanduser(f'~/fabric/download/{env.host}.txt')
    if os.path.exists(local_path):
        os.remove(local_path)
    remote_path = f'/tmp/{env.host}.txt'
    run(f'rm {remote_path}', warn_only=True)
    sql = (
        f'SELECT subject_identifier, consent_datetime INTO OUTFILE \'{remote_path}\' '
        'CHARACTER SET UTF8 '
        'FIELDS TERMINATED BY \'|\' ENCLOSED BY \'\' '
        'LINES TERMINATED BY \'\n\' '
        'FROM bcpp_subject_subjectconsent;')
    run(f'mysql -uroot -p edc -Bse \"{sql}\"')
    get(remote_path=f'/tmp/{env.host}.txt', local_path=local_path)


def list_tags_from(pip_file=None):
    data = {}
    with open(os.path.expanduser(pip_file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            package, tag = line.split('==')
            data.update({package.strip(): tag.strip()})
    return data


@task
def checkout_release(pip_file=None, branch=None, **kwargs):
    prepare_env(**kwargs)
    package_names = get_required_package_names()
    if branch:
        with lcd(f'~/source/{env.project_repo_name}'):
            local(f'git checkout {branch} # {env.project_repo_name}')
        for package_name in package_names:
            with lcd(f'~/source/{package_name}'):
                local(f'git checkout {branch} # {package_name}')
    else:
        tags = list_tags_from(pip_file=pip_file)
        with lcd(f'~/source/{env.project_repo_name}'):
            local(
                f'git checkout {env.project_release} # {env.project_repo_name}')
        for package_name in package_names:
            tag = tags.get(package_name)
            if tag:
                with lcd(f'~/source/{package_name}'):
                    local(f'git checkout {tag} # {package_name}')


@task
def checkout_branch(branch=None, **kwargs):
    prepare_env(**kwargs)
    package_names = get_required_package_names()
    if branch not in ['develop', 'master']:
        abort('Invalid branch. Got {branch}')
    else:
        with lcd(f'~/source/{env.project_repo_name}'):
            local(f'git checkout {branch} # {env.project_repo_name}')
        for package_name in package_names:
            with lcd(f'~/source/{package_name}'):
                local(f'git checkout {branch} # {package_name}')

@task
def update_r0135_task(**kwargs):

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


@task
def launch_webserver_bcpp(**kwargs):
    prepare_env(**kwargs)
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)
    launch_webserver()