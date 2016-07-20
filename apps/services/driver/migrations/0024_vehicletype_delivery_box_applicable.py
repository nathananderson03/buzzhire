# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0023_scooter_equivalent'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletype',
            name='delivery_box_applicable',
            field=models.BooleanField(default=False, help_text=b'Whether or not delivery boxes are relevant to this type of vehicle.'),
            preserve_default=True,
        ),
    ]
