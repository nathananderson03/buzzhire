# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

# Copy these from the model, as eventually we'll delete them from there
VEHICLE_TYPE_MOTORCYCLE = 'MC'
VEHICLE_TYPE_BICYCLE = 'BI'
VEHICLE_TYPE_CAR = 'CA'
VEHICLE_TYPE_VAN = 'VA'

def create_vehicle_types(apps, schema_editor):
    Driver = apps.get_model('driver', 'Driver')
    VehicleType = apps.get_model('driver', 'VehicleType')
    VALUES_MAP = {
        VEHICLE_TYPE_BICYCLE: 'Bicycle',
        VEHICLE_TYPE_MOTORCYCLE: 'Motorcycle/scooter',
        VEHICLE_TYPE_CAR: 'Car',
        VEHICLE_TYPE_VAN: 'Van',
    }

    for old_value, new_title in VALUES_MAP.items():
        vehicle_type = VehicleType.objects.create(title=new_title)
        # Update existing drivers
        for driver in Driver.objects.filter(
                                        vehicle_types_old__contains=old_value):
            driver.vehicle_types.add(vehicle_type)

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0010_auto_20150408_1555'),
    ]

    operations = [
        migrations.RunPython(create_vehicle_types),
    ]
