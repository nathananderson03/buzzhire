# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0006_freelancer_travel_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='travel_distance',
            field=models.PositiveSmallIntegerField(default=5, help_text=b'The maximum distance you are prepared to travel to a job.', choices=[(1, 'One mile'), (2, 'Two miles'), (5, 'Five miles'), (10, '10 miles'), (20, '20 miles'), (50, '50 miles')]),
            preserve_default=True,
        ),
    ]
