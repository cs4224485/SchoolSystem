# Generated by Django 2.1.1 on 2019-04-23 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0086_auto_20190423_1352'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='grade',
            table='Grade',
        ),
        migrations.AlterModelTable(
            name='schoolinfo',
            table='SchoolInfo',
        ),
        migrations.AlterModelTable(
            name='stuclass',
            table='StuClass',
        ),
    ]
