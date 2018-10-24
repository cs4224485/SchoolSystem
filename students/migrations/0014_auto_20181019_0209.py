# Generated by Django 2.1.1 on 2018-10-19 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_auto_20181017_0629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinnerinfo',
            name='student',
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='interior_student_id',
            field=models.CharField(default=1, max_length=255, unique=True, verbose_name='内部学生ID'),
        ),
        migrations.DeleteModel(
            name='StudentInnerInfo',
        ),
    ]
