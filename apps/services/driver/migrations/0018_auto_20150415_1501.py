# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0017_auto_20150415_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drivervehicletype',
            options={'ordering': ('vehicle_type__title',)},
        ),
        migrations.AlterField(
            model_name='drivervehicletype',
            name='delivery_box',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'What size delivery box does your vehicle have? (Scooters, motorcycles and bicycles only.)', verbose_name=b'Minimum delivery box size', choices=[(0, b'None'), (2, b'Standard'), (4, b'Pizza')]),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='drivervehicletype',
            unique_together=set([('driver', 'vehicle_type')]),
        ),
    ]
