# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0019_auto_20150818_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='last_applied',
            field=models.DateField(default=datetime.date(2015, 9, 11), auto_now_add=True),
            preserve_default=False,
        ),
    ]
