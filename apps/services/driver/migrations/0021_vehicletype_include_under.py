# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0020_auto_20150415_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletype',
            name='include_under',
            field=models.ForeignKey(blank=True, to='driver.VehicleType', help_text=b'Whether to include this under another vehicle type on job requests.', null=True),
            preserve_default=True,
        ),
    ]
