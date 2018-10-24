# Generated by Django 2.1.1 on 2018-10-18 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0029_auto_20181018_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='main_campus',
            field=models.IntegerField(choices=[(1, '本部'), (2, '分校或校区')], default=None, verbose_name='是本部还是校区'),
        ),
    ]
