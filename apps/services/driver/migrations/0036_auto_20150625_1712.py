# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0035_datamigration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driving_experience_old_2',
            field=models.PositiveSmallIntegerField(default=1, null=True, blank=True, choices=[(0, b'Less than 1 year'), (1, b'1 - 3 years'), (3, b'3 - 5 years'), (5, b'More than 5 years')]),
            preserve_default=True,
        ),
    ]
