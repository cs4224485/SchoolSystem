# Generated by Django 2.1.1 on 2019-02-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0013_remove_familyvisitrecord_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='familyvisitrecord',
            name='create_time',
            field=models.DateField(auto_created=True, default='2019-2-18', verbose_name='创建时间'),
        ),
    ]
