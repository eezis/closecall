# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_oauth_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBlogProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=150, null=True, verbose_name=b'Byline (how your name should appear)')),
                ('about_the_author', models.TextField(null=True, verbose_name=b"If you want an 'About The Author' section", blank=True)),
                ('up', models.OneToOneField(related_name='blogprofile', to='users.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='can_blog',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
