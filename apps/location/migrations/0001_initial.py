# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Postcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postcode', models.CharField(max_length=8, db_index=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'ordering': ['postcode'],
            },
            bases=(models.Model,),
        ),
    ]
