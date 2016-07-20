from fabric.api import *
from contextlib import contextmanager as _contextmanager
from fabric.contrib import files
from fabric import utils
import os
#==============================================================================
# Tasks which set up deployment environments
#==============================================================================

@task
def live():
    """
    Use the live deployment environment.
    """
    env.hosts = ['buzzhire.co']
    env.user = 'buzzhire'
    env.virtualenv_dir = '/home/buzzhire/.virtualenvs/live'
    env.code_dir = '/home/buzzhire/webapps/live/project'
    env.activate = 'source %s/bin/activate' % env.virtualenv_dir
    env.wsgi_reload_file = '/home/buzzhire/tmp/live.reload'
    env.nginx_process = 'live_nginx'
    env.uwsgi_process = 'live_uwsgi'
    env.huey_process = 'live_huey'
    env.backup_on_deploy = True
    env.django_configuration = 'Live'

@task
def stage():
    """
    Use the stage deployment environment.
    """
    env.hosts = ['stage.buzzhire.co']
    env.user = 'buzzhire'
    env.virtualenv_dir = '/home/buzzhire/.virtualenvs/stage'
    env.code_dir = '/home/buzzhire/webapps/stage/project'
    env.activate = 'source %s/bin/activate' % env.virtualenv_dir
    env.wsgi_reload_file = '/home/buzzhire/tmp/stage.reload'
    env.nginx_process = 'stage_nginx'
    env.uwsgi_process = 'stage_uwsgi'
    env.huey_process = 'stage_huey'
    env.backup_on_deploy = False
    env.django_configuration = 'Stage'


@task
def dev():
    """
    Use the development deployment environment.
    """
    env.hosts = ['dev.buzzhire.co']
    env.user = 'buzzhire'
    env.virtualenv_dir = '/home/buzzhire/.virtualenvs/dev'
    env.code_dir = '/home/buzzhire/webapps/dev/project'
    env.activate = 'source %s/bin/activate' % env.virtualenv_dir
    env.wsgi_reload_file = '/home/buzzhire/tmp/dev.reload'
    env.nginx_process = 'dev_nginx'
    env.uwsgi_process = 'dev_uwsgi'
    env.huey_process = 'dev_huey'
    env.backup_on_deploy = False
    env.django_configuration = 'Dev'

# Set the default environment.
dev()

@_contextmanager
def virtualenv():
    with cd(env.code_dir):
        with prefix('export DJANGO_CONFIGURATION=%s' % env.django_configuration):
            with prefix(env.activate):
                yield

@task
def reload_wsgi():
    """
    Graceful restart of wsgi server.
    """
    run('supervisorctl restart %s' % env.uwsgi_process)


@task
def reload_nginx():
    """
    Reload nginx config.
    """
    run('supervisorctl restart %s' % env.nginx_process)


@task
def restart_huey():
    """
    Restart the huey process.
    """
    run('supervisorctl restart %s' % env.huey_process)

@task
def deploy(skip_backup=False):
    """
    To deploy and skip backup:
      fab deploy:'skip'
    """
    with virtualenv():
        if env.backup_on_deploy and not skip_backup:
            dbbackup()

        run("git pull")
        run("pip install -r requirements.pip")

        run("./manage.py migrate")
        run('./manage.py collectstatic --noinput')
        reload_wsgi()
        restart_huey()

@task
def quickdeploy(skip_backup=False):
    """
    A quick deploy for front end changes.
    """
    with virtualenv():
        run("git pull")
        run('./manage.py collectstatic --noinput')
        reload_wsgi()

@task
def dbbackup():
    """Backs up the site database to Amazon S3.
    Doesn't back up uploaded files."""
    with virtualenv():
        run('./manage.py dbbackup --configuration=%s' \
                % env.django_configuration)

@task
def mediabackup():
    """Backs up uploaded files to Amazon S3."""
    with virtualenv():
        run('./manage.py sync_s3 --media-only --configuration=%s' \
                % env.django_configuration)
