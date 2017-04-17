from fabric.api import task, cd, prefix, run


@task
def fetch_map_images_task():
    """Fetches maps images for edc_map.

    For example:

       fab -P -R lentsweletau deploy.fetch_map_images_task --user=django

    """
    with cd('~/source/bcpp'):
        with prefix('source ~/.venvs/bcpp/bin/activate'):
            run('python manage.py fetch_map_images plot.plot 10')
