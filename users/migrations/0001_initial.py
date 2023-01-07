# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', models.CharField(max_length=120, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('first', models.CharField(max_length=50, null=True, blank=True)),
                ('last', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=120, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=30, null=True, blank=True)),
                ('email_incidents', models.BooleanField(default=True, verbose_name=b'Send Email When Incidents Occur In Your Area')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
