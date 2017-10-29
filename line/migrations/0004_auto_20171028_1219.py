# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0003_remove_touroffering_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='touroffering',
            name='user2',
        ),
        migrations.AddField(
            model_name='touroffering',
            name='user',
            field=models.ManyToManyField(through='line.Booking', to='line.User'),
        ),
    ]