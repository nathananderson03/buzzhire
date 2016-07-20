# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0016_auto_20150630_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='mobile',
            field=models.CharField(help_text=b'Your mobile phone number will be visible to clients on whose jobs you are booked.', max_length=13, validators=[django.core.validators.RegexValidator(b'^07[0-9 ]{9,11}$', b'Please enter a valid UK mobile phone number in the form 07xxx xxx xxx')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='published',
            field=models.BooleanField(default=True, help_text=b'Whether or not the freelancer is matched with jobs.'),
            preserve_default=True,
        ),
    ]
