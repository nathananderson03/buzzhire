# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0047_auto_20150622_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='years_experience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Minimum years of experience', choices=[(0, b'No preference'), (1, b'1 year'), (3, b'3 years'), (5, b'5 years')]),
            preserve_default=True,
        ),
    ]
