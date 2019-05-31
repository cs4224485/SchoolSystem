# Generated by Django 2.1.1 on 2018-10-30 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0055_auto_20181029_0346'),
        ('students', '0023_auto_20181029_0153'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScaleQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ScaleSetting', verbose_name='对应量表')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.StudentInfo', verbose_name='对应学生')),
            ],
        ),
        migrations.CreateModel(
            name='ScaleValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale_stu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.ScaleQuestion', verbose_name='对相应的学生量表')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ScaleLineTitle', verbose_name='对应的行标题')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ScaleOptionDes', verbose_name='对应的值')),
            ],
        ),
    ]
