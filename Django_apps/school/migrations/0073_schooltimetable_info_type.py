# Generated by Django 2.1.1 on 2018-12-07 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0072_auto_20181206_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltimetable',
            name='info_type',
            field=models.SmallIntegerField(choices=[(1, '课程'), (2, '其他事件')], default=1, verbose_name='存储的类型'),
        ),
    ]
