# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200221_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserConcern',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('concern', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='concern_user')),
                ('concerned', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='concerned_user')),
            ],
            options={
                'verbose_name': '用户关注',
                'verbose_name_plural': '用户关注',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='userconcern',
            unique_together=set([('concerned', 'concern')]),
        ),
    ]
