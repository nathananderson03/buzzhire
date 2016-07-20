# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0050_auto_20150630_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='duration',
            field=models.PositiveSmallIntegerField(default=2, help_text=b'Length of the job, in hours.', validators=[django.core.validators.MinValueValidator(2)]),
            preserve_default=True,
        ),
    ]
