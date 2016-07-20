# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0014_driverjobrequest_own_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='comments',
            field=models.TextField(help_text=b'Any further information to tell the driver.', blank=True),
            preserve_default=True,
        ),
    ]
