# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0015_auto_20150625_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='mobile',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(b'^07[0-9 ]{9,11}$', b'Please enter a valid UK mobile phone number in the form 07xxx xxx xxx')]),
            preserve_default=True,
        ),
    ]
