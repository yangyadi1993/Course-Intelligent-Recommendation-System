# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0007_auto_20161130_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='positions',
        ),
    ]
