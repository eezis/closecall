# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=150, null=True, blank=True)),
                ('first', models.CharField(max_length=50, null=True, verbose_name=b'First Name', blank=True)),
                ('last', models.CharField(max_length=50, null=True, verbose_name=b'Last Name', blank=True)),
                ('email', models.CharField(max_length=150, null=True, verbose_name=b'Email Adress', blank=True)),
                ('message', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
