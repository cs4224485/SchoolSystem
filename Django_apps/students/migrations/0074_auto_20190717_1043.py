# Generated by Django 2.2.1 on 2019-07-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0073_auto_20190716_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='level_1_dimension',
            field=models.CharField(choices=[('base_info', '基本数据'), ('sport', '大运动'), ('language', '语言表达'), ('observe', '观察与评估记录')], max_length=64, verbose_name='一级维度'),
        ),
    ]
