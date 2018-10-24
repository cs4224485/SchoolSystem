# Generated by Django 2.1.1 on 2018-10-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0031_auto_20181018_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='school_type',
            field=models.IntegerField(blank=True, choices=[(1, '公立'), (2, '民办')], default=None, null=True, verbose_name='学校类型'),
        ),
    ]
