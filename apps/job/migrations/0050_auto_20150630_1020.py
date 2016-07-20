# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0049_auto_20150625_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='comments',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
