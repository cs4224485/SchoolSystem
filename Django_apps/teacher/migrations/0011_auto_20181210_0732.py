# Generated by Django 2.1.1 on 2018-12-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0010_auto_20181127_0726'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.AlterField(
            model_name='teacherinfo',
            name='course',
            field=models.ManyToManyField(blank=True, null=True, to='school.Course', verbose_name='老师所带科目'),
        ),
    ]