# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 08:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0015_keyword'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='question',
            new_name='faq',
        ),
    ]
