# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0030_auto_20151205_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='timestr',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Approximate Time of Incident', blank=True),
            preserve_default=True,
        ),
    ]
