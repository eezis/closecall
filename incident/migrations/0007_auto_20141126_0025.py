# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0006_auto_20141120_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='what',
            field=models.TextField(help_text=b'Describe the incident', blank=True),
            preserve_default=True,
        ),
    ]
