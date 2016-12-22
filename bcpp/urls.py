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

from bcpp.views import SearchPlotView, HomeView, SearchHouseholdView, EnumerationDashboardView

from edc_base.views import LogoutView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('plot/', include('plot.urls')),
    url('household/', include('household.urls')),
    url('member/', include('member.urls')),
    url('subject/', include('bcpp_subject.urls')),
    url(r'^plot_search/(?P<page>\d+)/', SearchPlotView.as_view(), name='plot_search_url'),
    url(r'^plot_search/', SearchPlotView.as_view(), name='plot_search_url'),
    url(r'^bhs_search/$', SearchHouseholdView.as_view(), name='bhs_subject_search'),
    url(r'^enumeration_dashboard/$', EnumerationDashboardView.as_view(), name='enumeration_dashboard_url'),
    url(r'^subject_search/$', SearchHouseholdView.as_view(), name='subject_search'),
    url(r'^household_search/(?P<page>\d+)/', SearchHouseholdView.as_view(), name='household_search'),
    url(r'^household_search/$', SearchHouseholdView.as_view(), name='household_search'),
    url(r'^edc/', include('edc_base.urls', 'edc-base')),
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'', HomeView.as_view(), name='home_url'),
]
