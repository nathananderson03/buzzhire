# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0029_data_migration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverjobrequest',
            old_name='driving_experience',
            new_name='driving_experience_old',
        ),
    ]
