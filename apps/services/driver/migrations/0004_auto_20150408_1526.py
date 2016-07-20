# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0003_auto_20150325_1242'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='driving_experience',
            new_name='driving_experience_old',
        ),
    ]
