# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
        migrations.AlterModelOptions(
            name='inthenews',
            options={'verbose_name': 'In The News', 'verbose_name_plural': 'In The News'},
        ),
        migrations.AddField(
            model_name='inthenews',
            name='url',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
