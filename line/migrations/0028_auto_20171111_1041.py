# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 02:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0027_unknownquestion_hit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('push_date', models.DateTimeField(default=datetime.datetime(2017, 11, 11, 2, 41, 30, 374248, tzinfo=utc), verbose_name='push_date')),
                ('rate', models.DecimalField(decimal_places=2, default=0.8, max_digits=3)),
                ('seat', models.IntegerField(default=2)),
                ('quota', models.IntegerField(default=4)),
                ('tourOffering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.TourOffering')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='line.Discount'),
        ),
    ]
