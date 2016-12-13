from django.conf.urls import url

from .admin_site import bcpp_lab_admin

urlpatterns = [
    url(r'^admin/', bcpp_lab_admin.urls),
]
