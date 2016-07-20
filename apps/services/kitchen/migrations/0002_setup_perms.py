# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    add_admin_perms(apps.get_model('kitchen', 'KitchenJobRequest'))
    add_admin_perms(apps.get_model('kitchen', 'KitchenFreelancer'))

class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
