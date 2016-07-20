# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def datamigration(apps, schema_editor):
    add_admin_perms(apps.get_model('cleaner', 'CleanerPayGrade'))

class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0006_auto_20150821_1503'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
