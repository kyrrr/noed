# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0051_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytweet',
            name='text_summart',
            field=models.TextField(default=None, null=True),
        ),
    ]