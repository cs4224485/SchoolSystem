# Generated by Django 2.1.1 on 2018-10-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0021_auto_20181017_0746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolinfo',
            name='is_main_campus',
        ),
        migrations.AddField(
            model_name='schoolinfo',
            name='main_campus',
            field=models.IntegerField(choices=[(1, '本部'), (2, '分校或校区')], default=1, verbose_name='是本部还是校区'),
        ),
    ]
