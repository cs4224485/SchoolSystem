# Generated by Django 2.1.1 on 2019-04-09 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0049_auto_20190409_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthrecord',
            name='measure_type',
            field=models.IntegerField(blank=True, choices=[(1, '校测'), (2, '自测')], default=1, null=True, verbose_name='测试类型'),
        ),
    ]
