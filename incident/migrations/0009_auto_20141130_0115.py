# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0008_auto_20141126_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='color',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='id_it_by',
            field=models.CharField(max_length=250, null=True, verbose_name=b'List any special identifying characteristics of vehicle, if any', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='license_certain',
            field=models.CharField(max_length=20, null=True, verbose_name=b"License plate (use this input field if you are certain of the plate's numbers)", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='license_uncertain',
            field=models.CharField(max_length=150, null=True, verbose_name=b'License plate (use this input field if you are pretty sure, but not certain', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='make',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='model',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='vehicle_description',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='date',
            field=models.DateField(null=True, verbose_name=b'Date of Incident', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='time',
            field=models.TimeField(null=True, verbose_name=b'Approximate Time of Incident', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='what',
            field=models.TextField(verbose_name=b'Describe What Happened', blank=True),
            preserve_default=True,
        ),
    ]
