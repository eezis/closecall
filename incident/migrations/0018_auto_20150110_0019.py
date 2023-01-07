# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0017_auto_20141230_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='address',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='position',
            field=geoposition.fields.GeopositionField(max_length=42, null=True),
            preserve_default=True,
        ),
    ]
