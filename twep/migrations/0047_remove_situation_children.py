# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0046_auto_20170503_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation',
            name='children',
        ),
    ]