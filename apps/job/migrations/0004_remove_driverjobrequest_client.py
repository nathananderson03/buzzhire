# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_auto_20150401_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='client',
        ),
    ]
