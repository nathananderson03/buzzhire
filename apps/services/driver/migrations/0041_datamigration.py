# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def datamigration(apps, schema_editor):
    from apps.services.driver.models import FlexibleVehicleType

    DriverPayGrade = apps.get_model('driver', 'DriverPayGrade')
    # If there are no pay grades already, create some
    if not DriverPayGrade.objects.exists():
        # Pay, years experience, vehicle type title
        ITEMS = (
            (9.50, 0, 'Motorcycle'),
            (8.25, 3, None),
            (9.75, 3, 'Motorcycle'),
            (8.50, 3, 'Bicycle'),
            (9.50, 0, 'Car'),
            (9.75, 3, 'Car'),
            (10.00, 0, 'Van'),
            (11.00, 3, 'Van'),
            (8.25, 0, 'Bicycle'),
            (8.00, 0, None),
        )
        for min_client_pay_per_hour, years_experience, vehicle_type_title in ITEMS:

            if vehicle_type_title:
                vehicle_type_id = FlexibleVehicleType.objects.get(
                                                title=vehicle_type_title).id
            else:
                vehicle_type_id = None
            DriverPayGrade.objects.create(
                min_client_pay_per_hour=min_client_pay_per_hour,
                min_client_pay_per_hour_currency='GBP',
                years_experience=years_experience,
                vehicle_type_id=vehicle_type_id)
            print 'Created driver pay grade.'

class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0040_auto_20150821_1506'),
    ]

    operations = [
        migrations.RunPython(datamigration)
    ]
