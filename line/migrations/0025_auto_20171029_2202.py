# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0024_auto_20171029_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touroffering',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
