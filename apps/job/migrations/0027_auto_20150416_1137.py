# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0026_auto_20150416_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequest',
            name='client_pay_per_hour',
            field=djmoney.models.fields.MoneyField(default=Decimal('8.5'), help_text=b'How much you will pay per hour, for each driver.', max_digits=5, decimal_places=2, default_currency=b'GBP'),
            preserve_default=True,
        ),
    ]
