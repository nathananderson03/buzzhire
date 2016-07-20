# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.location.models import Postcode

def create_postcode(apps, schema_editor):
    if not Postcode.objects.exists():
        Postcode.objects.create(compressed_postcode='SW1A1AA')

class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_auto_20150417_0943'),
        ('job', '0029_remove_jobrequest_postcode'),
    ]

    operations = [
        migrations.RunPython(create_postcode),
        migrations.AddField(
            model_name='jobrequest',
            name='postcode',
            field=models.ForeignKey(default=lambda: Postcode.objects.all()[0].pk, to='location.Postcode'),
            preserve_default=False,
        ),
    ]
