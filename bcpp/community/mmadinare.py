from .base import *

MYSQL_CONF = 'mmadinare.conf'
ETC_DIR = '/etc'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

CURRENT_MAP_AREA = 'bokaa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, APP_NAME, CURRENT_MAP_AREA, MYSQL_CONF),
        },
    },
}

DEVICE_ID = '98'
DEVICE_ROLE = 'NodeServer'
