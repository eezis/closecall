# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0005_auto_20141126_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inthenews',
            options={'ordering': ['-report_on', '-created'], 'verbose_name': 'In The News', 'verbose_name_plural': 'In The News'},
        ),
        migrations.AddField(
            model_name='announcement',
            name='tags',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='announcement',
            name='tldr',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tldr',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inthenews',
            name='tags',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
    ]
