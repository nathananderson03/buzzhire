# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=True, help_text=b'Whether or not the freelancer shows up in search results. Note it is still possible for members of the public to view the freelancer if they know the link.')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('mobile', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(b'^07[0-9 ]*$', b'Please enter a valid UK mobile phone number in the form 07xxx xxx xxx')])),
                ('english_fluency', models.CharField(max_length=2, choices=[(b'BA', b'Basic'), (b'CO', b'Conversational'), (b'FL', b'Fluent'), (b'NA', b'Native')])),
                ('eligible_to_work', models.BooleanField(default=False, verbose_name=b'I am eligible to work in the UK.')),
                ('phone_type', models.CharField(blank=True, max_length=2, choices=[(b'AN', b'Android'), (b'IP', b'iPhone'), (b'WI', b'Windows'), (b'OT', b'Other smartphone'), (b'NS', b'Non smartphone')])),
                ('days_available', multiselectfield.db.fields.MultiSelectField(blank=True, help_text=b'Which days of the week are you available to work?', max_length=27, choices=[(b'mon', b'Monday'), (b'tue', b'Tuesday'), (b'wed', b'Wednesday'), (b'thu', b'Thursday'), (b'fri', b'Friday'), (b'sat', b'Saturday'), (b'sun', b'Sunday')])),
                ('hours_available', multiselectfield.db.fields.MultiSelectField(blank=True, help_text=b'What are your preferred working hours?', max_length=11, choices=[(b'MO', b'Mornings'), (b'AF', b'Afternoons'), (b'EV', b'Evenings'), (b'NI', b'Night')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'ordering': ('last_name',),
            },
            bases=(models.Model,),
        ),
    ]
