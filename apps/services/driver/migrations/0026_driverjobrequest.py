# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    """Moves DriverJobRequest from job app.
    See http://stackoverflow.com/questions/25648393/how-to-move-a-model-between-two-django-apps-django-1-7/26472482#26472482
    """

    dependencies = [
        ('job', '0043_move_driverjobrequest'),
        ('driver', '0025_datamigration'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='DriverJobRequest',
            fields=[
                ('jobrequest_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='job.JobRequest')),
                ('minimum_delivery_box', models.PositiveSmallIntegerField(default=0, help_text=b'For scooters, motorcycles and bicycles, the minimum delivery box size.', choices=[(0, b'None'), (2, b'Standard'), (4, b'Pizza')])),
                ('driving_experience', models.PositiveSmallIntegerField(default=0, verbose_name=b'Minimum driving experience', choices=[(0, b'Less than 1 year'), (1, b'1 - 3 years'), (3, b'3 - 5 years'), (5, b'More than 5 years')])),
                ('own_vehicle', models.BooleanField(default=True, verbose_name=b'The driver must supply their own vehicle.')),
                ('vehicle_type', models.ForeignKey(related_name='jobrequests', blank=True, to='driver.FlexibleVehicleType', help_text=b'Which type of vehicle would be appropriate for the job. ', null=True)),
                ('vehicle_types_old', models.ManyToManyField(related_name='jobrequests_old', null=True, to='driver.VehicleType', blank=True)),
            ],
            options={
            },
            bases=('job.jobrequest',),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]