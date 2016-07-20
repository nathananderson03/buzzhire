# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def types_to_type(apps, schema_editor):
    DriverJobRequest = apps.get_model('job', 'DriverJobRequest')
    FlexibleVehicleType = apps.get_model('driver', 'FlexibleVehicleType')
    for jobrequest in DriverJobRequest.objects.all():
        try:
            vehicle_type = jobrequest.vehicle_types_old.all()[0]
            jobrequest.vehicle_type = FlexibleVehicleType.objects.get(
                                                            pk=vehicle_type.pk)
            jobrequest.save()
        except IndexError:
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0035_auto_20150511_1640'),
    ]

    operations = [
        migrations.RunPython(types_to_type, lambda x, y: None)
    ]
