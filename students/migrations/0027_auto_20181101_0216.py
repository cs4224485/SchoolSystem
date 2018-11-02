# Generated by Django 2.1.1 on 2018-11-01 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0059_auto_20181031_1001'),
        ('students', '0026_auto_20181031_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graduateinstitutions',
            name='name',
        ),
        migrations.AddField(
            model_name='graduateinstitutions',
            name='school_name',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.SchoolInfo', verbose_name='学校名称'),
        ),
        migrations.AlterField(
            model_name='familyinfo',
            name='language',
            field=models.IntegerField(blank=True, choices=[(1, '中文普通话'), (2, '中文方言'), (3, '英语'), (4, '其他外语')], default=1, null=True, verbose_name='家庭语言'),
        ),
    ]