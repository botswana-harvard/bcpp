from .base import *

MYSQL_CONF = 'molapowabojang.conf'

CURRENT_MAP_AREA = 'molapowabojang'

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
