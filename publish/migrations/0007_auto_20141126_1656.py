# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0006_auto_20141126_1627'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ['-start_on_date', '-created'], 'verbose_name': 'Announcement', 'verbose_name_plural': 'Announcements'},
        ),
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-publish_date', '-created'], 'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='publish_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='end_on_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='start_on_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
