# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200220_1827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name_plural': '文章评论', 'verbose_name': '文章评论'},
        ),
        migrations.AddField(
            model_name='article',
            name='comment_count',
            field=models.IntegerField(verbose_name='评论数', default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='down_count',
            field=models.IntegerField(verbose_name='踩数', default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='up_count',
            field=models.IntegerField(verbose_name='点赞数', default=0),
        ),
        migrations.AlterField(
            model_name='comments',
            name='parent_comment',
            field=models.ForeignKey(blank=True, to='blog.Comments', null=True),
        ),
    ]
