# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_scooter(apps, schema_editor):
    VehicleType = apps.get_model('driver', 'VehicleType')
    VehicleType.objects.filter(title='Motorcycle/scooter').update(
                                                            title='Motorcycle')
    VehicleType.objects.create(title='Scooter')

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0014_auto_20150414_0920'),
    ]

    operations = [
        migrations.RunPython(add_scooter)
    ]
