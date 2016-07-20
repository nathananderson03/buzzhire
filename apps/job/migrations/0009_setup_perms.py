# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    """Adds ability for site admin to create, edit and delete job requests.
    """
    JobRequest = apps.get_model('job', 'JobRequest')
    add_admin_perms(JobRequest)

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_auto_20150402_1543'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
