# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0003_setup_perms'),
        ('booking', '0002_setup_perms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monday_early_morning', models.BooleanField(default=True, help_text=b'2am - 7am')),
                ('monday_morning', models.BooleanField(default=True, help_text=b'7am - 12pm')),
                ('monday_afternoon', models.BooleanField(default=True, help_text=b'12pm - 5pm')),
                ('monday_evening', models.BooleanField(default=True, help_text=b'5pm - 10pm')),
                ('monday_night', models.BooleanField(default=True, help_text=b'10pm - 2am')),
                ('tuesday_early_morning', models.BooleanField(default=True, help_text=b'2am - 7am')),
                ('tuesday_morning', models.BooleanField(default=True, help_text=b'7am - 12pm')),
                ('tuesday_afternoon', models.BooleanField(default=True, help_text=b'12pm - 5pm')),
                ('tuesday_evening', models.BooleanField(default=True, help_text=b'5pm - 10pm')),
                ('tuesday_night', models.BooleanField(default=True, help_text=b'10pm - 2am')),
                ('freelancer', models.OneToOneField(to='freelancer.Freelancer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
