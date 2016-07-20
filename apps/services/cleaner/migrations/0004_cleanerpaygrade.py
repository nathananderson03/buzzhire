# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cleaner', '0003_auto_20150803_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanerPayGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('years_experience', models.PositiveSmallIntegerField(verbose_name=b'Minimum years of experience', choices=[(0, b'No preference'), (1, b'1 year'), (3, b'3 years'), (5, b'5 years')])),
                ('min_client_pay_per_hour_currency', djmoney.models.fields.CurrencyField(default=b'GBP', max_length=3, editable=False, choices=[(b'GBP', 'Pound Sterling')])),
                ('min_client_pay_per_hour', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('9'), max_digits=5, validators=[django.core.validators.MinValueValidator(9.0)], verbose_name=b'Minimum client cost per hour', default_currency=b'GBP')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
