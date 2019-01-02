# Generated by Django 2.1.1 on 2018-12-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0004_auto_20181219_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechatbindinfo',
            name='salt',
            field=models.CharField(max_length=32, verbose_name='用于加密'),
        ),
        migrations.AlterField(
            model_name='wechatbindinfo',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '正常'), (2, '异常')], default=1, verbose_name='账号状态'),
        ),
    ]
