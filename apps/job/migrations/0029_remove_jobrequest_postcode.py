# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0028_auto_20150416_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequest',
            name='postcode',
        ),
    ]
