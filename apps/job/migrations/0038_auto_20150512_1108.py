# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0037_jobrequest_tips_included'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_types_old',
            field=models.ManyToManyField(related_name='jobrequests_old', null=True, to='driver.VehicleType', blank=True),
            preserve_default=True,
        ),
    ]
