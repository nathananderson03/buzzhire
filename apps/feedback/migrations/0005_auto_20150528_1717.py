# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_bookingfeedback_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingfeedback',
            options={'ordering': ('-date',)},
        ),
    ]
