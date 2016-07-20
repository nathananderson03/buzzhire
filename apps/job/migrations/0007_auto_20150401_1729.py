# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_auto_20150401_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverjobrequest',
            name='pay_per_hour',
            field=djmoney.models.fields.MoneyField(default=Decimal('0.0'), max_digits=5, decimal_places=2, default_currency=b'GBP'),
            preserve_default=True,
        ),
    ]
