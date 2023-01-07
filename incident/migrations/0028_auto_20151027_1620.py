# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incident', '0027_auto_20150526_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='cited',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incident',
            name='cited_note',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='what',
            field=models.TextField(verbose_name=b'\nNow describe what happened. Be factual, include direction of travel for cyclists and vehicles. Example: <p style="font-size:0.90em;margin-top:10px;margin-left:24px;\n    margin-right:30px;">\n\n    I was traveling southbound on Westminster Road, two other cyclists were riding immediately behind me. The driver of a white pickup truck, also traveling south,\n    started to honk his horn at us . . . your specifics details . . . </p>\n    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;">There was very little traffic on the road at the time of the encounter. The lighting was good,\n    all cyclists were inside the bike lane. </p>\n\n    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;"><i>\n    <span style="color:red">If you know the identity and home address of the driver, please do not include that information\n    in this report. You can email me that information (closecalldatabase@gmail.com) and I will include it in the non-public notes.</span></i>\n    </p>\n\n    <p style="font-size:0.90em;margin-top:10px;margin-left:24px;margin-right:30px;"><i>\n    If you have <span style="color:red">VIDEO</span> that you have posted to youtube, vimeo or a similar location, please email the URL to me. If you have a <span style="color:red">PICTURE</span> or two to accompany your report please email those as well closecalldatabase@gmail.\n    I will embed them in the report.\n    </i></p>\n\n\nTell your story with enough context so that it can be understood by cyclists that were not there and may be unfamiliar with the location.\n'),
            preserve_default=True,
        ),
    ]
