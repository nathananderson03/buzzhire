# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0013_auto_20150414_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='vehicle_types_own',
            field=models.ManyToManyField(related_name='drivers_own', verbose_name=b'Vehicles I can provide myself', to='driver.VehicleType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driver',
            name='vehicle_types_able',
            field=models.ManyToManyField(related_name='drivers_able', verbose_name=b'Vehicles I can drive', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
