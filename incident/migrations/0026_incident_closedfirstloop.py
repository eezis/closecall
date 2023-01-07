# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0025_auto_20150522_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='closedfirstloop',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
