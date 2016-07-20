# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete drivers."
    DriverJobRequest = apps.get_model('driver', 'DriverJobRequest')
    add_admin_perms(DriverJobRequest)

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0026_driverjobrequest'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
