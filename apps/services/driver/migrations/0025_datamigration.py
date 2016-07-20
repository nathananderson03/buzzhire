# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    """Set motorcycles, bicycles and scooters as having delivery boxes
    as relevant."""
    VehicleType = apps.get_model('driver', 'VehicleType')
    TYPES = ('Bicycle', 'Motorcycle', 'Scooter')
    VehicleType.objects.filter(title__in=TYPES).update(
                                                delivery_box_applicable=True)
class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0024_vehicletype_delivery_box_applicable'),
    ]

    operations = [
        migrations.RunPython(datamigration),
    ]
