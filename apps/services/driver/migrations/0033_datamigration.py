# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    # Go through all the drivers and set the legacy phone type field (which
    # is on the Freelancer model) to the new phone type field.
    Driver = apps.get_model('driver', 'Driver')
    for driver in Driver.objects.all():
        driver.phone_type = driver.phone_type_old
        driver.save()

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0032_auto_20150625_1607'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
