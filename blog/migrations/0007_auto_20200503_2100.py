# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200409_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='profile',
            field=models.CharField(null=True, max_length=128),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='profile',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
