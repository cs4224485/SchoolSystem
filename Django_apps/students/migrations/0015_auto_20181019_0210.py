# Generated by Django 2.1.1 on 2018-10-19 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20181019_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='interior_student_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='内部学生ID'),
        ),
    ]
