# Generated by Django 2.1.1 on 2019-04-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0083_auto_20190409_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='choicetable',
            name='is_required',
            field=models.SmallIntegerField(choices=[(1, '必填'), (2, '选填')], default=1, verbose_name='是否必填'),
        ),
        migrations.AddField(
            model_name='scalesetting',
            name='is_required',
            field=models.SmallIntegerField(choices=[(1, '必填'), (2, '选填')], default=1, verbose_name='是否必填'),
        ),
        migrations.AddField(
            model_name='settingtofield',
            name='is_required',
            field=models.SmallIntegerField(choices=[(1, '必填'), (2, '选填')], default=1, verbose_name='是否必填'),
        ),
    ]
