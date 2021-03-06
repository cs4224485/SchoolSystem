# Generated by Django 2.1.1 on 2018-10-18 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0030_auto_20181018_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='school_layer',
            field=models.IntegerField(choices=[(1, '幼儿园'), (2, '小学'), (3, '初中'), (4, '高中阶段'), (5, '九年一惯制'), (6, '中等职业学校'), (7, '十二年一贯制')], default=None, verbose_name='学校层级'),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='school_type',
            field=models.IntegerField(choices=[(1, '公立'), (2, '民办')], default=None, verbose_name='学校类型'),
        ),
    ]
