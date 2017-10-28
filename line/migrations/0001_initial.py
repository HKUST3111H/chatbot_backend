# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('duration', models.IntegerField(default=3)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TourOffering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_date', models.DateTimeField(verbose_name='offer date')),
                ('hotel', models.CharField(max_length=200)),
                ('capacity_min', models.IntegerField(default=5)),
                ('capacity_max', models.IntegerField(default=30)),
                ('guide_name', models.CharField(max_length=20)),
                ('guide_line', models.CharField(max_length=50)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.Tour')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone_num', models.CharField(max_length=20)),
                ('age', models.CharField(max_length=20)),
                ('state', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='touroffering',
            name='users',
            field=models.ManyToManyField(to='line.User'),
        ),
    ]
