# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0036_vehicle_types_to_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='tips_included',
            field=models.BooleanField(default=False, verbose_name=b'Inclusive of tips'),
            preserve_default=True,
        ),
    ]
