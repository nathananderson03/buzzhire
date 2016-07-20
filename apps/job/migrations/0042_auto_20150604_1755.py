# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0041_save_end_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='end_datetime',
            field=models.DateTimeField(help_text=b'Automatically generated, the time when this job request finishes.'),
            preserve_default=True,
        ),
    ]
