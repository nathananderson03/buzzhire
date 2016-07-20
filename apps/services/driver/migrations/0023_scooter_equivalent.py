# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def scooter_equivalent(apps, schema_editor):
    "Makes scooters the equivalents to motorcycles."
    VehicleType = apps.get_model('driver', 'VehicleType')
    scooter = VehicleType.objects.get(title='Scooter')
    scooter.equivalent_to = VehicleType.objects.get(
                                            title='Motorcycle')
    scooter.save()

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0022_auto_20150511_1544'),
    ]

    operations = [
        migrations.RunPython(scooter_equivalent)
    ]
