# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0003_auto_20141126_0145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inthenews',
            options={'ordering': ['created'], 'verbose_name': 'In The News', 'verbose_name_plural': 'In The News'},
        ),
        migrations.AddField(
            model_name='inthenews',
            name='city',
            field=models.CharField(max_length=80, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='country',
            field=models.CharField(max_length=80, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='occurred_on',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='report_on',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='state',
            field=models.CharField(max_length=80, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='tldr',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='zipcode',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
