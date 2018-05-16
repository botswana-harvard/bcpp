from .base import *

MYSQL_CONF = 'mysql.conf'

CURRENT_MAP_AREA = 'ramokgonami'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, APP_NAME, MYSQL_CONF),
        },
    },
}

DEVICE_ID = config['edc_device'].get('device_id')
DEVICE_ROLE = 'Client'
