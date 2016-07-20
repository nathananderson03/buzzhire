# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0010_freelancer_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancer',
            name='published',
            field=models.BooleanField(default=True, help_text=b'Whether or not the freelancer shows up in search results.'),
            preserve_default=True,
        ),
    ]
