# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0011_create_vehicle_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='vehicle_types_old',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=11, choices=[(b'BI', b'Bicycle'), (b'MC', b'Motorcycle/scooter'), (b'CA', b'Car'), (b'VA', b'Van')]),
            preserve_default=True,
        ),
    ]
