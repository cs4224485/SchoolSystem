# Generated by Django 2.2.1 on 2019-07-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0074_auto_20190717_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='level_2_dimension',
            field=models.SmallIntegerField(blank=True, choices=[(1, '力量'), (2, '平衡'), (3, '速度'), (4, '特殊问题')], null=True, verbose_name='二级维度'),
        ),
    ]