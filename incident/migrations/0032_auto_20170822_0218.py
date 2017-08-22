# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0031_incident_timestr'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='driver_fault',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='has_pic',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='has_video',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='utility',
            field=models.DecimalField(default=0.0, null=True, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='utility_comment',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Utility Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='utility_defect',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Utility Defect', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='youtubeurl',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='danger_assessment',
            field=models.IntegerField(default=5, null=True, verbose_name=b'Danger Assessment', choices=[(10, b'Extremely Dangerous - The action could have caused a fatility'), (8, b'Very Dangerous - The action could have caused serious injury or death'), (5, b'Dangerous - the action could have caused serious injury'), (3, b'Somewhat Dangerous - the action could have caused moderate injuries'), (1, b'The action was not very dangerous, but is still a cause for concern')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='id_it_by',
            field=models.CharField(max_length=250, null=True, verbose_name=b'Identifying Characteristics', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='license_certain',
            field=models.CharField(max_length=20, null=True, verbose_name=b'License Plate - CERTAIN', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='license_uncertain',
            field=models.CharField(max_length=150, null=True, verbose_name=b'License Plate - UNCERTAIN', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='threat_assessment',
            field=models.CharField(default=b'Aggressive', max_length=50, null=True, verbose_name=b'Threat Assessment', choices=[(b'Belligerent', b'Belligerent - the driver was malicious and undertook deliberate actions that purposefully put lives at risk'), (b'Threatening', b'Threatening - the driver create a dangerous situation and delivered a measured threat (close, but not too close)'), (b'Aggressive', b'Aggressive - the driver was trying to scare, harass or intimidate (yelled, honked, etc)'), (b'Careless', b'Careless - the driver caused a problem but it wasnt deliberately hostile and may have been accidental'), (b'Thoughtless', b'Just Plain Stupid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='what',
            field=models.TextField(verbose_name=b'What Happened'),
            preserve_default=True,
        ),
    ]
