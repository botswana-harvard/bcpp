import os

from fabric.api import env, task, run, cd, get
from fabric.colors import red
from fabric.utils import warn, abort

from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.mysql import put_mysql_conf, put_my_cnf
from edc_fabric.fabfile.pip import get_pip_list
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import launch_webserver, update_settings,\
    rsync_deployment_root
from edc_fabric.fabfile.virtualenv import create_venv

from .utils import update_bcpp_conf
from fabric.operations import local
from edc_fabric.fabfile.files.dmg import mount_dmg
from edc_fabric.fabfile.gunicorn.tasks import install_gunicorn
from fabric.context_managers import prefix, lcd
from edc_fabric.fabfile.pip.tasks import get_required_package_names


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
def update_temp_task(**kwargs):

    prepare_env(**kwargs)
#     mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
#               dmg_passphrase=env.crypto_keys_passphrase)
    install_gunicorn()
    launch_webserver()

    # put_my_cnf()

    # run('brew services restart mysql')


@task
def update_r0133_task(bootstrap_filename=None, skip_update_project_repo=None, skip_venv=None, map_area=None, **kwargs):

    release = '0.1.33'
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
