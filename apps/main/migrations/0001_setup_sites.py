# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def setup_sites(apps, schema_editor):
    from django.contrib.sites.models import Site
    from django.conf import settings
    Site.objects.filter(id=1).update(name=settings.SITE_TITLE,
                                     domain=settings.DOMAIN)

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '__first__'),
    ]

    operations = [
        migrations.RunPython(setup_sites),
    ]
