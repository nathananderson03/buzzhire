# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='friday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='friday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='friday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='friday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='friday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='saturday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='saturday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='saturday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='saturday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='saturday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='sunday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='sunday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='sunday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='sunday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='sunday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='thursday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='availability',
            name='wednesday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='monday_afternoon',
            field=models.BooleanField(default=True, help_text=b'12pm - 5pm', choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='monday_early_morning',
            field=models.BooleanField(default=True, help_text=b'2am - 7am', choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='monday_evening',
            field=models.BooleanField(default=True, help_text=b'5pm - 10pm', choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='monday_morning',
            field=models.BooleanField(default=True, help_text=b'7am - 12pm', choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='monday_night',
            field=models.BooleanField(default=True, help_text=b'10pm - 2am', choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='tuesday_afternoon',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='tuesday_early_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='tuesday_evening',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='tuesday_morning',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='availability',
            name='tuesday_night',
            field=models.BooleanField(default=True, choices=[(True, b'Available'), (False, b'Not available')]),
            preserve_default=True,
        ),
    ]
