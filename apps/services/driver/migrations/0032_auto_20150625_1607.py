# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0031_data_migration'),
        ('freelancer', '0015_auto_20150625_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drivervehicletype',
            options={'ordering': ('vehicle_type__title',), 'verbose_name': 'driver vehicle'},
        ),
        migrations.AddField(
            model_name='driver',
            name='phone_type',
            field=models.CharField(blank=True, max_length=2, choices=[(b'AN', b'Android'), (b'IP', b'iPhone'), (b'WI', b'Windows'), (b'OT', b'Other smartphone'), (b'NS', b'Non smartphone')]),
            preserve_default=True,
        ),
    ]
