# Generated by Django 2.1.1 on 2018-10-17 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0017_schoolinfo_is_main_campus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='is_main_campus',
            field=models.BooleanField(verbose_name='是否是本部'),
        ),
    ]
