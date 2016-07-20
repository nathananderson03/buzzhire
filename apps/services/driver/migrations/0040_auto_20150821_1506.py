# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0039_datamigration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driverpaygrade',
            options={'ordering': ('-years_experience',)},
        ),
    ]
