# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0019_auto_20150413_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='driving_experience',
        ),
    ]
