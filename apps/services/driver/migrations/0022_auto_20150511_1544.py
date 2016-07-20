# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0021_vehicletype_include_under'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexibleVehicleType',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('driver.vehicletype',),
        ),
        migrations.RemoveField(
            model_name='vehicletype',
            name='include_under',
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='equivalent_to',
            field=models.ForeignKey(related_name='equivalent_children', blank=True, to='driver.VehicleType', help_text=b'Another vehicle type this should be treated as equivalent to in certain circumstances, such as in job requests.', null=True),
            preserve_default=True,
        ),
    ]
