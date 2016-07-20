# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0004_cleanerpaygrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cleanerpaygrade',
            name='years_experience',
            field=models.PositiveSmallIntegerField(verbose_name=b'Years of experience', choices=[(0, b'No preference'), (1, b'1 year'), (3, b'3 years'), (5, b'5 years')]),
            preserve_default=True,
        ),
    ]
