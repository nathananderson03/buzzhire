# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0009_auto_20150506_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='photo',
            field=models.ImageField(upload_to=b'freelancer/photos/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
