# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0023_scooter_equivalent'),
        ('job', '0034_auto_20150511_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverjobrequest',
            name='vehicle_type',
            field=models.ForeignKey(related_name='jobrequests', to='driver.FlexibleVehicleType', help_text=b'Which type of vehicle would be appropriate for the job. ', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_types_old',
            field=models.ManyToManyField(related_name='jobrequests_old', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
