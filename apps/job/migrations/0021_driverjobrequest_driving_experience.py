# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0020_remove_driverjobrequest_driving_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='driving_experience',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'Minimum driving experience', choices=[(0, b'Less than 1 year'), (1, b'1 - 3 years'), (3, b'3 - 5 years'), (5, b'More than 5 years')]),
            preserve_default=True,
        ),
    ]
