# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_client_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(help_text=b'The name of your company', max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
