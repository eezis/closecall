# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0010_auto_20141221_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.CharField(max_length=150, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='the_post',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
