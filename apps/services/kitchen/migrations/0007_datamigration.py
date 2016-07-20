# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def datamigration(apps, schema_editor):
    add_admin_perms(apps.get_model('kitchen', 'KitchenPayGrade'))

class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0006_auto_20150818_1509'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
