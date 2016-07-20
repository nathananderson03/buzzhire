# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    """Adds ability for site admin to create, edit and delete driver
    job requests.
    """
    try:
        DriverJobRequest = apps.get_model('job', 'DriverJobRequest')
        add_admin_perms(DriverJobRequest)
    except:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
