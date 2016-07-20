# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0024_auto_20150414_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='minimum_delivery_box',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'For scooters, motorcycles and bicycles, the minimum delivery box size.', choices=[(0, b'None'), (2, b'Standard'), (4, b'Pizza')]),
            preserve_default=True,
        ),
    ]
