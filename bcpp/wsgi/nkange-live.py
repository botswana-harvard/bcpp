import os

from django.core.wsgi import get_wsgi_application

os.environ.update(DJANGO_SETTINGS_MODULE="bcpp.community.nkange")

application = get_wsgi_application()