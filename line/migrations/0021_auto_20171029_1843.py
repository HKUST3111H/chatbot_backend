# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0020_touroffering_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touroffering',
            name='price',
            field=models.IntegerField(default=-1),
        ),
    ]