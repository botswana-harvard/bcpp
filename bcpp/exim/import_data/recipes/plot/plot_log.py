from django.apps import apps as django_apps

from plot.models import Plot, PlotLog

from ...recipe import site_recipes, Recipe


def post_import_handler():
    app_config = django_apps.get_app_config('plot')
    for plot in Plot.objects.exclude(
            pk__in=[obj.plot.pk for obj in PlotLog.objects.all()]):
        if not app_config.excluded_plot(plot):
            PlotLog.objects.create(
                plot=plot, report_datetime=plot.report_datetime)

site_recipes.register(Recipe(
    model_name='plot.plotlog',
    post_import_handler=post_import_handler))
