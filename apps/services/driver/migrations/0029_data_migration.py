# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def data_migration(apps, schema_editor):
    # Move the driving experience over to the field on the freelancer model
    try:
        Driver = apps.get_model('driver', 'Driver')
        for driver in Driver.objects.all():
            driver.years_experience = driver.driving_experience_old_2
            driver.save()
    except:
        print('Skipping driving experience data migration.')
    

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0028_auto_20150624_1022'),
    ]

    operations = [
        migrations.RunPython(data_migration)
    ]
