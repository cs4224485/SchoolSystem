# Generated by Django 2.1.1 on 2019-03-25 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0046_auto_20190307_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentparents',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], default=None, null=True, verbose_name='性别'),
        ),
    ]
