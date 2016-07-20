# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0021_driverjobrequest_driving_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='vehicle_types',
        ),
    ]
