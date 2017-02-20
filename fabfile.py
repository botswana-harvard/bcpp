from fabric.api import local

from fabric.api import *
from fabric.utils import error, warn
from fabric.contrib.files import exists
from fabric.colors import green, red, blue
from __builtin__ import True

hosts = {'django@192.168.1.68:22': 'Aish1uch'}

env.hosts = [host for host in hosts.keys()]
env.passwords = hosts

env.virtualenv_name = 'bcpp'
env.source_dir = '/Users/django/source'

env.update_repo = False

env.create_db = False
env.drop_and_create_db = True

class FabricException(Exception):
    pass

@task
def remove_virtualenv(name=None):
    result = run('rmvirtualenv {}'.format(env.virtualenv_name))
    if result.succeeded:
        print(blue('removing {} virtualenv .....'.format(env.virtualenv_name)))
        print(green('{} virtualenv removed.'.format(env.virtualenv_name)))
    else:
        error(result)

@task
def create_virtualenv():
    print(blue('creating {} virtualenv .....'.format(env.virtualenv_name)))
    run('mkvirtualenv {}'.format(env.virtualenv_name))
    print(green('{} virtualenv created.'.format(env.virtualenv_name)))
    print(green(''))

@task
def clone_bcpp():
    run('mkdir -p {}'.format(env.source_dir))
    with cd(env.source_dir):
        run('git clone https://github.com/botswana-harvard/bcpp.git')

@task
def install_requirements():
    with cd('{}/{}'.format(env.source_dir, 'bcpp')):
        run('pip install -r requirements.txt')

@task
def create_database():
    if env.drop_and_create_db:
        if console.confirm('Are you sure you want to drop database {} and create it? y/n'.format('bcpp'),
                               default=False):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

@task
def migrate():
    with prefix('workon bcpp'):
        with cd ('/Users/django/source/bcpp/nginx_deployment'):
            run('cp bcpp.conf {}/{}'.format(env.source_dir, 'bcpp'))
            run('cp bcpp.conf {}/{}'.format(env.source_dir, 'bcpp'))
            run('python manage.py migrate --run-syncdb')

@task
def setup_nginx():
    sudo("mkdir -p /usr/local/etc/nginx/sites-available")
    sudo("mkdir -p /usr/local/etc/nginx/sites-enabled")
    with cd(env.source_dir):
        pass

    #
    put('*.py', 'cgi-bin/')

@task
def deploy(server=None):
    with settings(abort_exception=FabricException):
        try:
            if not env.update_repo:
                execute(remove_virtualenv)
                execute(create_virtualenv)
                execute(clone_bcpp)
                execute(install_requirements)
                execute(migrate)
            else:
                pass
        except FabricException as e:
            print(e)
