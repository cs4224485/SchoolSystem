# Generated by Django 2.1.1 on 2018-10-19 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_studentinfo_interior_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='interior_student_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='内部学生ID'),
        ),
    ]
