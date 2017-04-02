# import configparser
# import os
#
# from fabric.api import *
#
# from bcpp_fabric.new.fabfile import update_env
#
# CONFIG_PATH = '~/source/bcpp-fabric/bcpp_fabric/new/fabric.conf'
#
# if os.path.exists(os.path.expanduser('~/deployment/fabric.conf')):
#     config_path = os.path.expanduser('~/deployment/fabric.conf')
# elif CONFIG_PATH:
#     config_path = os.path.expanduser(CONFIG_PATH)
# else:
#     config_path = os.path.expanduser('/etc/bcpp/fabric.conf')
# update_env(config_path=CONFIG_PATH)
#
# config = configparser.RawConfigParser()
# if os.path.exists(os.path.expanduser('~/deployment/hosts.conf')):
#     config_path = os.path.expanduser('~/deployment/hosts.conf')
# elif CONFIG_PATH:
#     config_path = os.path.expanduser(CONFIG_PATH)
# else:
#     config_path = os.path.expanduser('/etc/bcpp/fabric.conf')
#
# print('Reading hosts from ', config_path)
#
# config.read(config_path)
#
# for host, pwd in config['hosts'].items():
#     if '@' not in host:
#         host = '{}@{}'.format(env.user, host)
#     env.passwords.update({'{}:22'.format(host): pwd})
#     env.hosts.append(host)
# print('hosts', env.hosts)
# print('passwords', env.passwords)
#
# env.device_ids = {}
# for host, device_id in config['device_ids'].items():
#     env.device_ids.update({host: device_id})
#
# print('device_ids', env.device_ids)
