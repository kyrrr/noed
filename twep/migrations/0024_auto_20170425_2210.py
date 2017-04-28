# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 22:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0023_auto_20170425_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='keyword',
            name='category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.KeywordCategory'),
        ),
    ]
