# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0005_freelancer_postcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='travel_distance',
            field=models.PositiveSmallIntegerField(default=5, help_text=b'The maximum distance you are prepared to travel to a job.', choices=[(1, 'one miles'), (2, 'two miles'), (5, 'five miles'), (10, b'10 miles'), (20, b'20 miles'), (50, b'50 miles')]),
            preserve_default=True,
        ),
    ]
