# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0016_auto_20150414_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverVehicleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('own_vehicle', models.BooleanField(default=False, verbose_name=b'I can provide this vehicle on a job.')),
                ('delivery_box', models.PositiveSmallIntegerField(default=0, help_text=b'For scooters, motorcycles and bicycles, what is the minimum delivery box size?', verbose_name=b'Minimum delivery box size', choices=[(0, b'None'), (2, b'Standard'), (4, b'Pizza')])),
                ('driver', models.ForeignKey(to='driver.Driver')),
                ('vehicle_type', models.ForeignKey(to='driver.VehicleType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='driver',
            name='own_vehicle',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='vehicle_types_able',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='vehicle_types_own',
        ),
        migrations.AddField(
            model_name='driver',
            name='vehicle_types',
            field=models.ManyToManyField(help_text=b'Which vehicles you are able and licensed to drive. You do not need to provide the vehicle for the booking.', related_name='drivers', verbose_name=b'Vehicles', through='driver.DriverVehicleType', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
