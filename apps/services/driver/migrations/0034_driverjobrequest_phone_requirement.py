# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0033_datamigration'),
        ('job', '0049_auto_20150625_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='phone_requirement',
            field=models.CharField(default=b'NR', help_text=b'Whether the driver needs a smart phone to do this job (for example, if you need them to run an app).', max_length=2, choices=[(b'NR', b'No smart phone needed'), (b'AY', b'Any smart phone'), (b'AN', b'Android'), (b'IP', b'iPhone'), (b'WI', b'Windows')]),
            preserve_default=True,
        ),
    ]
