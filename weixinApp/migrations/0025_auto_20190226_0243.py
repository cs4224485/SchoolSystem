# Generated by Django 2.1.1 on 2019-02-26 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0024_auto_20190225_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familyvisitrecord',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='familyvisitrecord',
            name='visit_date',
        ),
        migrations.AddField(
            model_name='schedule',
            name='create_time',
            field=models.DateField(auto_now=True, verbose_name='创建时间'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='date',
            field=models.DateField(default='1993-04-13', verbose_name='日期时间'),
        ),
    ]