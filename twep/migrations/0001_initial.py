# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('V', 'Violation'), ('D', 'Danger'), ('L', 'Location'), ('S', 'Status'), ('H', 'Happy'), ('U', 'Unknown')], default='U', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MyTweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.CharField(max_length=200)),
                ('twitter_msg_id', models.CharField(max_length=20, unique=True)),
                ('screen_name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('reply_to', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('keywords', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='created at')),
                ('status', models.CharField(choices=[('RP', 'Reported'), ('IP', 'In Progress'), ('RS', 'Resolved'), ('U', 'Unknown')], default='RP', max_length=20)),
                ('danger', models.CharField(choices=[('ND', 'No Danger'), ('C', 'Caution'), ('D', 'Danger'), ('U', 'Unknown')], default='U', max_length=20)),
                ('tweets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twep.MyTweet')),
            ],
        ),
    ]
