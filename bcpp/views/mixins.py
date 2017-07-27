from django.apps import apps as django_apps


class AppConfigListboardUrlsViewMixin:

    """Adds listboard_url names for all BCPP apps"""

    dashboard_url_app_label = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            plot_dashboard_listboard_url_name=django_apps.get_app_config(
                'plot_dashboard').listboard_url_name,
            household_dashboard_listboard_url_name=django_apps.get_app_config(
                'household_dashboard').listboard_url_name,
            member_dashboard_listboard_url_name=django_apps.get_app_config(
                'member_dashboard').listboard_url_name,
            enumeration_listboard_url_name=django_apps.get_app_config(
                'enumeration').listboard_url_name,
            bcpp_subject_dashboard_listboard_url_name=django_apps.get_app_config(
                'bcpp_subject_dashboard').dashboard_url_name,
            enumeration_dashboard_url_name=django_apps.get_app_config(
                'enumeration').dashboard_url_name,
            dashboard_url_name=django_apps.get_app_config(
                self.dashboard_url_app_label).dashboard_url_name,
        )
        return context
