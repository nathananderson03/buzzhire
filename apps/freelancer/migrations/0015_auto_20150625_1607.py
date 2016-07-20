# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0014_freelancer_years_experience'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freelancer',
            old_name='phone_type',
            new_name='phone_type_old',
        ),
    ]
