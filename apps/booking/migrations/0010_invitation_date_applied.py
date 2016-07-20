# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20150625_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='date_applied',
            field=models.DateTimeField(help_text=b'When the freelancer applied to the job.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
