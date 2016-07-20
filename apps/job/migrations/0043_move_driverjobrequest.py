# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    """Moves the DriverJobRequest to the driver app.
    See http://stackoverflow.com/questions/25648393/how-to-move-a-model-between-two-django-apps-django-1-7/26472482#26472482
    """
    dependencies = [
        ('job', '0042_auto_20150604_1755'),
    ]

    database_operations = [
        migrations.AlterModelTable('DriverJobRequest',
                                   'driver_driverjobrequest')
    ]

    state_operations = [
        migrations.DeleteModel('DriverJobRequest')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]