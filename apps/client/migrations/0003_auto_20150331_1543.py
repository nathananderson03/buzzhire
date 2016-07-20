# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0002_setup_perms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(b'^07[0-9 ]*$', b'Please enter a valid UK mobile phone number in the form 07xxx xxx xxx')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'ordering': ('last_name',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='lead',
            name='more_information',
            field=models.TextField(help_text=b"If you like, tell us a little more about what you're looking for.", blank=True),
            preserve_default=True,
        ),
    ]
