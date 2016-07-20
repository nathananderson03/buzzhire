# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_setup_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingfeedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 28, 11, 2, 42, 626141), auto_now_add=True),
            preserve_default=False,
        ),
    ]
