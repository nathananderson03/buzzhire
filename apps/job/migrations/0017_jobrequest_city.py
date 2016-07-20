# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0016_auto_20150409_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='city',
            field=models.CharField(default=b'L', help_text=b'We currently only accept bookings in London.', max_length=1, choices=[(b'L', b'London')]),
            preserve_default=True,
        ),
    ]
