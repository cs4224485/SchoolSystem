# Generated by Django 2.1.1 on 2019-03-01 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0031_indexnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexnotification',
            name='is_display',
            field=models.BooleanField(default=True, verbose_name='是否在前端展示'),
        ),
    ]