# Generated by Django 2.1.1 on 2018-10-19 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0040_auto_20181019_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='title',
            field=models.IntegerField(choices=[(1, '一年级'), (2, '二年级'), (3, '三年级'), (4, '四年级'), (5, '五年级'), (6, '六年级'), (7, '初一'), (8, '初二')]),
        ),
    ]
