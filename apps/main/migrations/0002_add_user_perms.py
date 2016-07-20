# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from apps.core.perms import add_admin_perms

def setup_perms(apps, schema_editor):
    "Adds ability for site admin to create, edit and delete users."
    from django.contrib.auth.models import User
    add_admin_perms(User)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_setup_sites'),
    ]

    operations = [
        migrations.RunPython(setup_perms)
    ]
