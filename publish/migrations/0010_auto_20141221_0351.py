# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0009_inthenews_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='about_the_author',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
    ]
