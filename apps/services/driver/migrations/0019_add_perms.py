# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    """Adds ability for site admin to create, edit and delete vehicle types and
    driver vehicle types."""
    add_admin_perms((apps.get_model('driver', 'VehicleType'),
                     apps.get_model('driver', 'DriverVehicleType')))


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0018_auto_20150415_1501'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
