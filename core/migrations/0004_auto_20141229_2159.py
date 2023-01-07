# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141221_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinput',
            name='message',
            field=models.TextField(null=True, verbose_name=b'Your comment, question, or proposal'),
            preserve_default=True,
        ),
    ]
