# Generated by Django 2.1.1 on 2018-12-06 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0070_course_schooltimetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='schooltimetable',
            name='other_event',
            field=models.SmallIntegerField(blank=True, choices=[(1, '课间操'), (2, '午休')], default=1, null=True, verbose_name='学校其他事件'),
        ),
        migrations.AddField(
            model_name='schooltimetable',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.SchoolInfo', verbose_name='学校'),
        ),
        migrations.AddField(
            model_name='schooltimetable',
            name='single_double_week',
            field=models.SmallIntegerField(blank=True, choices=[(1, '单'), (2, '双')], default=1, null=True, verbose_name='课程单双周'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Course', verbose_name='课程'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='stu_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.StuClass', verbose_name='班级'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.TeacherInfo', verbose_name='代课老师'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='time_range',
            field=models.TimeField(verbose_name='时间段'),
        ),
        migrations.AlterField(
            model_name='schooltimetable',
            name='week',
            field=models.SmallIntegerField(blank=True, choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五')], null=True, verbose_name='星期'),
        ),
    ]
