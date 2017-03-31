# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='courses/default.png', upload_to='courses/%Y/%M/%D', verbose_name='logo'),
        ),
    ]
