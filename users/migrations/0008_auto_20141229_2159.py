# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20141221_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=120, null=True, verbose_name=b'City  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ NA if Not Applicable ]'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=50, null=True, verbose_name=b'State/Province/Region  &nbsp;&nbsp;&nbsp;&nbsp;[ NA if Not Applicable ]'),
            preserve_default=True,
        ),
    ]
