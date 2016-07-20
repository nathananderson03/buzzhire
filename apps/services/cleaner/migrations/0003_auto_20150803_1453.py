# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0002_setup_perms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cleaner',
            options={'verbose_name': 'cleaner'},
        ),
    ]
