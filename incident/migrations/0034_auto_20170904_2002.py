# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0033_auto_20170822_0223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='ee_show_youtube_vid',
            new_name='ee_show_video',
        ),
        migrations.RenameField(
            model_name='incident',
            old_name='show_youtube_vid',
            new_name='show_video',
        ),
        migrations.RenameField(
            model_name='incident',
            old_name='youtube_offensive_votes',
            new_name='video_offensive_votes',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='youtubeurl',
        ),
        migrations.AddField(
            model_name='incident',
            name='facebook_url',
            field=models.CharField(max_length=180, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='video_embed_string',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='vimeo_url',
            field=models.CharField(max_length=180, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='youtube_url',
            field=models.CharField(max_length=180, null=True, blank=True),
            preserve_default=True,
        ),
    ]
