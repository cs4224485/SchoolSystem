# Generated by Django 2.1.1 on 2018-12-28 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0073_schooltimetable_info_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltimetable',
            name='position',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='前端展示的位置'),
        ),
    ]