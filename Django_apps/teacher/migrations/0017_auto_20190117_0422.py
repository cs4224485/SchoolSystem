# Generated by Django 2.1.1 on 2019-01-17 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0016_auto_20190117_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherinfo',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别'),
        ),
    ]
