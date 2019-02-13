# Generated by Django 2.1.1 on 2019-01-28 03:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0079_auto_20190118_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolTimeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='开始时间')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='结束时间')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.SchoolInfo', verbose_name='学校')),
            ],
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='single_double_week',
            field=models.SmallIntegerField(choices=[(1, '每周'), (2, '单周'), (3, '双周')], default=1, verbose_name='课程单双周'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='time_range',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.SchoolTimeRange'),
        ),
    ]
