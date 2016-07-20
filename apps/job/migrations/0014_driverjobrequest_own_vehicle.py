# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0013_auto_20150408_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='own_vehicle',
            field=models.BooleanField(default=True, verbose_name=b'The driver must supply their own vehicle.'),
            preserve_default=True,
        ),
    ]
