# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0027_auto_20150416_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='start_time',
            field=models.TimeField(default=b'9:00 AM'),
            preserve_default=True,
        ),
    ]
