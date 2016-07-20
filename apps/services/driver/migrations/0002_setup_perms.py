# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete drivers."
    Driver = apps.get_model('driver', 'Driver')
    add_admin_perms(Driver)

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
