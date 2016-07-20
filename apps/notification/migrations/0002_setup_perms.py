# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def datamigration(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete notifications."
    add_admin_perms(apps.get_model('notification', 'Notification'))

class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
