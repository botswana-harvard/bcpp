
__all__ = ['deploy_client', 'dismount_keys', 'mount_keys']

import os
from io import StringIO
from fabric.api import task, env, cd, run
from fabric.contrib import django


from bcpp_fabric.new.fabfile import MACOSX
from bcpp_fabric.new.fabfile.crypto_keys import (
    mount_crypto_keys, dismount_crypto_keys)
from fabric.colors import red
from fabric.contrib.files import exists, contains

app_name = 'bcpp'

django.project(app_name)
django.settings_module('{}.settings'.format(app_name))

from django.conf import settings as django_settings


@task
def dismount_keys():
    """Dismount MACOSX dmg volume on remote host.
    """
    if not env.target_os == MACOSX:
        print(red('Incorrect operating system. Got {}'.format(env.target_os)))
    else:
        dismount_crypto_keys(key_volume=env.key_volume)


@task
def mount_keys():
    """Mount MACOSX dmg volume on remote host.
    """
    if not env.target_os == MACOSX:
        print(red('Incorrect operating system. Got {}'.format(env.target_os)))
    else:
        if django_settings.KEY_PATH == env.key_volume:
            mount_crypto_keys(dmg_filename=env.dmg_filename,
                              dmg_path=env.dmg_path)
            with cd(env.key_volume):
                run('ls user-*')
        else:
            print(red('Invalid key_path. Expected {}. Got {}'.format(
                env.key_volume, django_settings.KEY_PATH)))
