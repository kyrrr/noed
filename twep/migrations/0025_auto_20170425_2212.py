# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0024_auto_20170425_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='category',
        ),
        migrations.AddField(
            model_name='keywordcategory',
            name='words',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.Keyword'),
        ),
    ]