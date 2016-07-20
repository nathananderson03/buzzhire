# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0048_jobrequest_years_experience'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobrequest',
            old_name='phone_requirement',
            new_name='phone_requirement_old',
        ),
    ]
