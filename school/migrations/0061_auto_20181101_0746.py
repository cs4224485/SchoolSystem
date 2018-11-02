# Generated by Django 2.1.1 on 2018-11-01 07:46

from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0060_tableinfo_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableinfo',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.fields.CharField, related_name='for_student', to='students.StudentInfo', verbose_name='填表的学生'),
        ),
    ]
