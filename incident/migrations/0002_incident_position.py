# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='position',
            field=geoposition.fields.GeopositionField(default=(52.522906, 13.41156), max_length=42),
            preserve_default=False,
        ),
    ]
