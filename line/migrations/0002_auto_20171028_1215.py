# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_num', models.IntegerField(default=1)),
                ('child_num', models.IntegerField(default=0)),
                ('elder_num', models.IntegerField(default=0)),
                ('tour_fee', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('paid_fee', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('special_request', models.CharField(default='None', max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='touroffering',
            old_name='users',
            new_name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='tourOffering',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.TourOffering'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.User'),
        ),
        migrations.AddField(
            model_name='touroffering',
            name='user2',
            field=models.ManyToManyField(related_name='user2', through='line.Booking', to='line.User'),
        ),
    ]