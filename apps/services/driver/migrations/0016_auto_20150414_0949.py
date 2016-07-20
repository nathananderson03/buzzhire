# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0015_auto_20150414_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle_types_able',
            field=models.ManyToManyField(help_text=b'Which vehicles you are able and licensed to drive. You do not need to provide the vehicle for the booking.', related_name='drivers_able', verbose_name=b'Vehicles you can drive', to='driver.VehicleType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driver',
            name='vehicle_types_own',
            field=models.ManyToManyField(help_text=b'Which vehicles you can provide for a booking.', related_name='drivers_own', verbose_name=b'Vehicles you can provide', to='driver.VehicleType', blank=True),
            preserve_default=True,
        ),
    ]
