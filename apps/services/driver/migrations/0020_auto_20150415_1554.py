# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0019_add_perms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle_types',
            field=models.ManyToManyField(related_name='drivers', to='driver.VehicleType', through='driver.DriverVehicleType', blank=True, help_text=b'Which vehicles you are able and licensed to drive. You do not need to provide the vehicle for the booking.', verbose_name=b'Vehicles'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='drivervehicletype',
            name='vehicle_type',
            field=models.ForeignKey(help_text=b'Note: you may only create one vehicle of each type.', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
