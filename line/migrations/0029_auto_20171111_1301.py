# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 05:01
from __future__ import unicode_literals

from django.db import migrations, models
import line.models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0028_auto_20171111_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='push_date',
            field=models.DateTimeField(default=line.models.Discount.default_push_date, verbose_name='push_date'),
        ),
    ]
