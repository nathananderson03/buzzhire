# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from decimal import Decimal
import djmoney.models.fields

def delete_all_driverjobrequests(apps, schema_editor):
    """Deletes all driverjobrequests currently in the system."""
    DriverJobRequest = apps.get_model('job', 'DriverJobRequest')
    DriverJobRequest.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_client_perms'),
        ('job', '0007_auto_20150401_1729'),
    ]

    operations = [
        migrations.RunPython(delete_all_driverjobrequests),
        migrations.CreateModel(
            name='JobRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'OP', max_length=2, choices=[(b'OP', b'Open'), (b'CF', b'Confirmed'), (b'CP', b'Complete'), (b'CA', b'Cancelled')])),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('pay_per_hour_currency', djmoney.models.fields.CurrencyField(default=b'GBP', max_length=3, editable=False, choices=[(b'GBP', 'Pound Sterling')])),
                ('pay_per_hour', djmoney.models.fields.MoneyField(default=Decimal('0.0'), max_digits=5, decimal_places=2, default_currency=b'GBP')),
                ('date', models.DateField(default=datetime.date.today)),
                ('start_time', models.TimeField(default=datetime.datetime.now)),
                ('duration', models.PositiveSmallIntegerField(default=1, help_text=b'Length of the job, in hours.')),
                ('number_of_freelancers', models.PositiveSmallIntegerField(default=1, verbose_name=b'Number of people required', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('client', models.ForeignKey(related_name='job_requests', to='client.Client')),
            ],
            options={
                'ordering': ('-date_submitted',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='driverjobrequest',
            options={},
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='client',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='date',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='date_submitted',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='id',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='number_of_freelancers',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='pay_per_hour',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='pay_per_hour_currency',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='driverjobrequest',
            name='status',
        ),
        migrations.AddField(
            model_name='driverjobrequest',
            name='jobrequest_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='job.JobRequest'),
            preserve_default=False,
        ),
    ]
