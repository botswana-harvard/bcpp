from .base import *

MYSQL_CONF = 'bokaa.conf'
ETC_DIR = '/etc'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

CURRENT_MAP_AREA = 'bokaa'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, APP_NAME, MYSQL_CONF_FILES, MYSQL_CONF),
        },
    },
}

DEVICE_ID = '98'
DEVICE_ROLE = 'NodeServer'
