# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 19:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0006_remove_education_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user_profile',
            name='gender',
        ),
    ]
