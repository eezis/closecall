# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0002_auto_20141126_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inthenews',
            options={'ordering': ['-created'], 'verbose_name': 'In The News', 'verbose_name_plural': 'In The News'},
        ),
        migrations.AddField(
            model_name='inthenews',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inthenews',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
