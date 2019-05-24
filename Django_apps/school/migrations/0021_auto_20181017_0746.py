# Generated by Django 2.1.1 on 2018-10-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_auto_20181017_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='school_layer',
            field=models.IntegerField(choices=[(1, '幼儿园'), (2, '小学'), (3, '初中'), (4, '高中阶段'), (5, '九年一惯制'), (6, '中等职业学校'), (7, '十二年一贯制')], default=1, verbose_name='学校层级'),
        ),
    ]