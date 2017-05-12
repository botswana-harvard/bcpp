import os

from fabric.api import env, task, run, get
from fabric.colors import red
from fabric.context_managers import lcd
from fabric.contrib.project import rsync_project
from fabric.operations import local
from fabric.utils import warn, abort

from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.mysql.tasks import install_protocol_database
from edc_fabric.fabfile.pip import get_pip_list
from edc_fabric.fabfile.pip.tasks import get_required_package_names
from edc_fabric.fabfile.utils import launch_webserver

from ..prepare_env import prepare_env
from fabfile.utils import list_tags_from


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
def launch_webserver_bcpp(**kwargs):
    prepare_env(**kwargs)
    mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
              dmg_passphrase=env.crypto_keys_passphrase)
    launch_webserver()
