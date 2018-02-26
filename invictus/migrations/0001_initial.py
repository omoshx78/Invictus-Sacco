# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-14 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.IntegerField()),
                ('message', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member_reg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('dob', models.DateField(max_length=50)),
                ('idno', models.IntegerField()),
                ('member_no', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=20)),
                ('employer', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('religion', models.CharField(max_length=50)),
                ('kin_fullname', models.CharField(max_length=100)),
                ('kin_phone', models.IntegerField()),
                ('kin_id', models.IntegerField()),
                ('kin_relation', models.CharField(max_length=70)),
                ('datestamp', models.DateField()),
                ('transaction_reference', models.CharField(max_length=80)),
            ],
        ),
    ]
