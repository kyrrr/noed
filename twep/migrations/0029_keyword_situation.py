# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 18:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0028_auto_20170427_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='situation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.Situation'),
        ),
    ]