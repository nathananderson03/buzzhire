# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0006_datamigration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='waitingpaygrade',
            options={'ordering': ('-years_experience',)},
        ),
    ]
