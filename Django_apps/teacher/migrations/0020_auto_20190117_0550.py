# Generated by Django 2.1.1 on 2019-01-17 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0019_auto_20190117_0548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
    ]
