# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('freelancer', '0011_auto_20150528_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_freelancer.freelancer_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
