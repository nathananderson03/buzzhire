# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waiting', '0002_setup_perms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='waitingfreelancer',
            options={'verbose_name': 'waiter'},
        ),
    ]
