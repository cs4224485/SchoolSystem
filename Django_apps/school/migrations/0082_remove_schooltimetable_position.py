# Generated by Django 2.1.1 on 2019-04-01 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0081_auto_20190214_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schooltimetable',
            name='position',
        ),
    ]
