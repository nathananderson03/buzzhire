# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0008_auto_20150408_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='vehicle_types',
            new_name='vehicle_types_old',
        ),
    ]
