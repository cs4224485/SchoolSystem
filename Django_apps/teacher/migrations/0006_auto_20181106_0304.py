# Generated by Django 2.1.1 on 2018-11-06 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_auto_20181105_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classtoteacher',
            name='stu_class',
            field=models.ForeignKey(limit_choices_to={'school_id__in': ['115']}, on_delete=django.db.models.deletion.CASCADE, related_name='handle_class', to='school.StuClass', verbose_name='班级'),
        ),
    ]
