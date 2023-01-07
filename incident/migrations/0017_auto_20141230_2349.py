# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0016_auto_20141230_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='id_it_by',
            field=models.CharField(max_length=250, null=True, verbose_name=b'List any special identifying characteristics of vehicle and passengers that you observed', blank=True),
            preserve_default=True,
        ),
    ]
