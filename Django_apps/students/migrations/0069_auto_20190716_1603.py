# Generated by Django 2.2.1 on 2019-07-16 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0068_auto_20190716_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualityassessmentsource',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.StudentInfo', verbose_name='学生'),
        ),
    ]