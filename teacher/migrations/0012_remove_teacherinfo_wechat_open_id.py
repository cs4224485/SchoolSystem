# Generated by Django 2.1.1 on 2018-12-19 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0011_auto_20181210_0732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherinfo',
            name='wechat_open_id',
        ),
    ]
