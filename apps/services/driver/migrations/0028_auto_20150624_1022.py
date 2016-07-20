# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0027_perms'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='driving_experience',
            new_name='driving_experience_old_2',
        ),
    ]
