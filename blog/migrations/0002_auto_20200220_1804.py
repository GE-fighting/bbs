# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '文章',
                'verbose_name': '文章',
            },
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.TextField()),
                ('article', models.OneToOneField(to='blog.Article')),
            ],
            options={
                'verbose_name_plural': '文章详情',
                'verbose_name': '文章详情',
            },
        ),
        migrations.CreateModel(
            name='ArticleToTag',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('article', models.ForeignKey(to='blog.Article')),
            ],
            options={
                'verbose_name_plural': '文章-标签',
                'verbose_name': '文章-标签',
            },
        ),
        migrations.CreateModel(
            name='ArticleUpDown',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('is_up', models.BooleanField(default=True)),
                ('article', models.ForeignKey(to='blog.Article')),
            ],
            options={
                'verbose_name_plural': '文章点赞',
                'verbose_name': '文章点赞',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '文章分类',
                'verbose_name': '文章分类',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=225)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(to='blog.Article')),
                ('parent_comment', models.ForeignKey(null=True, to='blog.Comments')),
            ],
            options={
                'verbose_name_plural': '文章点赞',
                'verbose_name': '文章点赞',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '文章标签',
                'verbose_name': '文章标签',
            },
        ),
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name_plural': 'blog 站点', 'verbose_name': 'blog 站点'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '用户信息', 'verbose_name': '用户信息'},
        ),
        migrations.AddField(
            model_name='blog',
            name='site',
            field=models.CharField(unique=True, max_length=32, default=datetime.datetime(2020, 2, 20, 10, 3, 55, 748374, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='theme',
            field=models.CharField(max_length=32, default=datetime.datetime(2020, 2, 20, 10, 4, 16, 684633, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='blog',
            field=models.ForeignKey(to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='blog',
            field=models.ForeignKey(to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articletotag',
            name='tag',
            field=models.ForeignKey(to='blog.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, to='blog.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='desc',
            field=models.ForeignKey(to='blog.Blog'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', through='blog.ArticleToTag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together=set([('article', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='articletotag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
