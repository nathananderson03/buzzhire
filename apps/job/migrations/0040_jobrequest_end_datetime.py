# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0039_auto_20150528_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='end_datetime',
            field=models.DateTimeField(help_text=b'Automatically generated, the time when this job request finishes.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
