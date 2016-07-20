# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0007_datamigration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kitchenpaygrade',
            options={'ordering': ('-years_experience',)},
        ),
    ]
