# Generated by Django 2.1.1 on 2019-02-20 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0020_auto_20190220_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='familyvisitrecord',
            name='visit_time',
            field=models.TimeField(blank=True, null=True, verbose_name='访问时间'),
        ),
        migrations.AlterField(
            model_name='familyvisitrecord',
            name='visit_date',
            field=models.DateField(verbose_name='访问时间'),
        ),
    ]
