# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0004_search_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='activation_token',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user_profile',
            name='resume',
            field=models.FileField(null=True, upload_to='../media/files/'),
        ),
    ]
