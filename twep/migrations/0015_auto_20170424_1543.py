# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0014_auto_20170424_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mytweet',
            name='scanned',
        ),
        migrations.RemoveField(
            model_name='situation',
            name='created_at',
        ),
    ]
