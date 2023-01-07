# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141205_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_with',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='zipcode',
            field=models.CharField(max_length=30, null=True, verbose_name=b'Zip/Postal Code', blank=True),
            preserve_default=True,
        ),
    ]
