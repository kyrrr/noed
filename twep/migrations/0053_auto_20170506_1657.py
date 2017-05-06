# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0052_auto_20170506_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='mytweet',
            name='screen_name',
        ),
        migrations.AddField(
            model_name='mytweet',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.User'),
        ),
    ]