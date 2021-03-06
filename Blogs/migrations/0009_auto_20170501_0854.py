# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 08:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogs', '0008_auto_20170501_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='downvotes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='upvotes',
            field=models.ManyToManyField(blank=True, null=True, related_name='blog_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
