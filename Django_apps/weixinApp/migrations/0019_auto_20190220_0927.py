# Generated by Django 2.1.1 on 2019-02-20 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0018_familyvisitrecord_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familyvisitrecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.TeacherInfo', verbose_name='访问的老师'),
        ),
    ]
