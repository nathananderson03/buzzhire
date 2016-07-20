# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0030_jobrequest_postcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='client_pay_per_hour',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('8.5'), max_digits=5, validators=[django.core.validators.MinValueValidator(8.5)], help_text=b'How much you will pay per hour, for each driver.', default_currency=b'GBP'),
            preserve_default=True,
        ),
    ]
