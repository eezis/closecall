# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0004_auto_20141126_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inthenews',
            options={'ordering': ['report_on', 'created'], 'verbose_name': 'In The News', 'verbose_name_plural': 'In The News'},
        ),
        migrations.AlterField(
            model_name='inthenews',
            name='occurred_on',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inthenews',
            name='report_on',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
