"""bcpp URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from edc_appointment.admin_site import edc_appointment_admin
from edc_base.views import LogoutView, LoginView
from edc_lab.admin_site import edc_lab_admin
from edc_metadata.admin_site import edc_metadata_admin
from edc_registration.admin_site import edc_registration_admin
from edc_sync.admin import edc_sync_admin
from edc_sync_files.admin_site import edc_sync_files_admin
from edc_map.admin import edc_map_admin
from edc_identifier.admin_site import edc_identifier_admin

from plot.admin_site import plot_admin
from household.admin_site import household_admin
from member.admin_site import member_admin

from bcpp_subject.admin_site import bcpp_subject_admin

from .views import HomeView, AdministrationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', edc_appointment_admin.urls),
    url(r'^admin/', plot_admin.urls),
    url(r'^admin/', household_admin.urls),
    url(r'^admin/', member_admin.urls),
    url(r'^admin/', bcpp_subject_admin.urls),
    url(r'^admin/', edc_lab_admin.urls),
    url(r'^admin/', edc_identifier_admin.urls),
    url(r'^admin/', edc_map_admin.urls),
    url(r'^admin/', edc_metadata_admin.urls),
    url(r'^admin/', edc_registration_admin.urls),
    url(r'^admin/', edc_sync_admin.urls),
    url(r'^admin/', edc_sync_files_admin.urls),
    url(r'^admininistration/', AdministrationView.as_view(),
        name='administration_url'),
    url('plot/', include('plot.urls')),
    url('household/', include('household.urls')),
    url('member/', include('member.urls')),
    url('enumeration/', include('enumeration.urls')),
    url('subject/', include('bcpp_subject.urls')),
    url('follow/', include('bcpp_follow.urls')),
    url(r'^appointment/',
        include('edc_appointment.urls')),
    url(r'^edc/', include('edc_base.urls')),
    url(r'^edc_consent/', include('edc_consent.urls')),
    url(r'^edc_device/', include('edc_device.urls')),
    url(r'^edc_lab/', include('edc_lab.urls')),
    url(r'^edc_label/', include('edc_label.urls')),
    url(r'^edc_map/', include('edc_map.urls')),
    url(r'^edc_metadata/', include('edc_metadata.urls')),
    url(r'^edc_protocol/', include('edc_protocol.urls')),
    url(r'^edc_registration/',
        include('edc_registration.urls')),
    url(r'^edc_sync/', include('edc_sync.urls')),
    url(r'^edc_sync_files/', include('edc_sync_files.urls')),
    url(r'^edc_visit_schedule/',
        include('edc_visit_schedule.urls')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(
        pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
