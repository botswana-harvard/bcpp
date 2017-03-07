from django.apps import apps as django_apps


class AppConfigListboardUrlsViewMixin:

    """Adds listboard_url names for all BCPP apps"""

    dashboard_url_app_label = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            plot_listboard_url_name=django_apps.get_app_config('plot').listboard_url_name,
            household_listboard_url_name=django_apps.get_app_config('household').listboard_url_name,
            member_listboard_url_name=django_apps.get_app_config('member').listboard_url_name,
            enumeration_listboard_url_name=django_apps.get_app_config('enumeration').listboard_url_name,
            bcpp_subject_listboard_url_name=django_apps.get_app_config('bcpp_subject').dashboard_url_name,
            enumeration_dashboard_url_name=django_apps.get_app_config('enumeration').dashboard_url_name,
            dashboard_url_name=django_apps.get_app_config(self.dashboard_url_app_label).dashboard_url_name,
        )
        return context
