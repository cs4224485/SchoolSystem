# Generated by Django 2.2.1 on 2019-11-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0044_askforleave_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='askforleave',
            name='detail',
            field=models.TextField(default=1111, max_length=255, verbose_name='请假详情'),
        ),
    ]