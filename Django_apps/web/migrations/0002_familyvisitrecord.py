# Generated by Django 2.1.1 on 2019-02-18 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0040_auto_20190218_0652'),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyVisitRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField(verbose_name='访问时间')),
                ('reason', models.TextField(max_length=150, verbose_name='访问原因')),
                ('state', models.SmallIntegerField(choices=[(1, '预约中'), (2, '已完成'), (3, '已取消')], default=1, verbose_name='预约状态')),
                ('relate_parents', models.ManyToManyField(to='students.StudentParents', verbose_name='关联家长')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.StudentInfo', verbose_name='对应学生')),
            ],
            options={
                'db_table': 'FamilyVisitRecord',
            },
        ),
    ]
