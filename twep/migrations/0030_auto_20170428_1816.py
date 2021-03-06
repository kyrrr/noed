# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0029_keyword_situation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation',
            name='danger_level',
        ),
        migrations.RemoveField(
            model_name='situation',
            name='status',
        ),
        migrations.AddField(
            model_name='mytweet',
            name='prevalent_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.KeywordCategory'),
        ),
        migrations.AddField(
            model_name='situation',
            name='description',
            field=models.CharField(default=None, max_length=140, null=True),
        ),
    ]
