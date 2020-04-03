# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200220_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 20, 10, 22, 56, 806419, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatars/default.jpg', upload_to='avatars/', verbose_name='头像'),
        ),
    ]
