# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0033_auto_20150507_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverjobrequest',
            old_name='vehicle_types',
            new_name='vehicle_types_old',
        ),
    ]
