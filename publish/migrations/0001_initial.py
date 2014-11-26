# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('the_announcement', models.TextField()),
                ('start_on_date', models.DateField(null=True)),
                ('end_on_date', models.DateField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('the_post', models.TextField()),
                ('tags', models.CharField(max_length=50, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'BlogPost',
                'verbose_name_plural': 'BlogPosts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InTheNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('summary', models.TextField()),
                ('tags', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'MODELNAME',
                'verbose_name_plural': 'MODELNAMEs',
            },
            bases=(models.Model,),
        ),
    ]
