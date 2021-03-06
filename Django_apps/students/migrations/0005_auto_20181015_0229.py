# Generated by Django 2.1.1 on 2018-10-15 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20181012_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthinfo',
            name='blood_type',
            field=models.IntegerField(blank=True, choices=[(1, 'A'), (2, 'B'), (3, 'O'), (4, 'AB'), (5, '不知道')], null=True, verbose_name='血型'),
        ),
        migrations.AlterField(
            model_name='healthinfo',
            name='disability',
            field=models.IntegerField(choices=[(1, '无'), (2, '视力'), (3, '听力语言'), (4, '智力'), (5, '肢体'), (6, '精神')], default=1, null=True, verbose_name='残疾'),
        ),
    ]
