# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0012_auto_20141205_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='danger_assessment',
            field=models.IntegerField(default=5, null=True, verbose_name=b'Danger Assessment: In your opinion, this encounter was . . . ', choices=[(10, b'Extremely Dangerous - The action could have caused a fatility'), (8, b'Very Dangerous - The action could have caused serious injury or death'), (5, b'Dangerous - the action could have caused serious injury'), (3, b'Somewhat Dangerous - the action could have caused moderate injuries'), (1, b'The action was not very dangerous, but is still a cause for concern')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='threat_assessment',
            field=models.CharField(default=b'Aggressive', max_length=50, null=True, verbose_name=b'Threat Assessment: In your opinion the motorist/person in question was being . . .', choices=[(b'Belligerent', b'Belligerent'), (b'Threatening', b'Threatening'), (b'Aggressive', b'Aggressive'), (b'Careless', b'Careless'), (b'Stupid', b'Just Plain Stupid')]),
            preserve_default=True,
        ),
    ]
