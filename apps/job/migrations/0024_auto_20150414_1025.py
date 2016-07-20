# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0023_driverjobrequest_vehicle_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='vehicle_types',
            field=models.ManyToManyField(help_text=b'Which types of vehicle would be appropriate for the job. (N.B. if you require a specific mixture of vehicles, such as one car and one van, then you should create these as separate bookings.)', related_name='jobrequests', to='driver.VehicleType'),
            preserve_default=True,
        ),
    ]
