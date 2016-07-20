# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0003_auto_20150625_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kitchenfreelancer',
            options={'verbose_name': 'chef', 'verbose_name_plural': 'kitchen staff'},
        ),
    ]
