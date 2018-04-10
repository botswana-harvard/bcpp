from ..settings import *

MYSQL_CONF = 'mysql.conf'

CURRENT_MAP_AREA = 'mmankgodi'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, APP_NAME, MYSQL_CONF),
        },
    },
}

DEVICE_ID = '98'
DEVICE_ROLE = 'NodeServer'
