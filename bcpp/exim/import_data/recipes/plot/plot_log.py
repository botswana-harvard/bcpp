from django.apps import apps as django_apps

from plot.models import Plot, PlotLog

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


def post_import_handler():
    app_config = django_apps.get_app_config('plot')
    for plot in Plot.objects.exclude(
            pk__in=[obj.plot.pk for obj in PlotLog.objects.all()]):
        if not app_config.excluded_plot(plot):
            PlotLog.objects.create(
                plot=plot, report_datetime=plot.report_datetime)

site_recipes.register(ModelRecipe(
    model_name='plot.plotlog',
    old_model_name='bcpp_household.plotlog',
    post_import_handler=post_import_handler))


sql = (
    'INSERT INTO plot_plotlog (id, plot_id, report_datetime, revision, created, '
    'modified, hostname_created, hostname_modified, user_created, user_modified) '
    'SELECT REPLACE(uuid(),' -
    ','') as id, p.id as plot_id, p.report_datetime, '
    'p.revision, p.created, p.modified, p.hostname_created, p.hostname_modified, '
    '\'erikvw\' as user_created, \'erikvw\' as user_modified '
    'FROM plot_plot as p '
    'LEFT JOIN plot_plotlog as pl on pl.plot_id=p.id WHERE pl.id is NULL;'
)
