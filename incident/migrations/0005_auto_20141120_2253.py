# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0004_incident_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incident',
            options={'ordering': ['-created'], 'verbose_name': 'Incident', 'verbose_name_plural': 'Incidents'},
        ),
    ]
