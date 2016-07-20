# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_driverjobrequest_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='date',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverjobrequest',
            name='duration',
            field=models.PositiveSmallIntegerField(default=1, help_text=b'Length of the job, in hours.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverjobrequest',
            name='start_time',
            field=models.TimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
