# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0019_auto_20170424_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytweet',
            name='keyword',
            field=models.ManyToManyField(default=None, to='twep.Keyword'),
        ),
    ]
