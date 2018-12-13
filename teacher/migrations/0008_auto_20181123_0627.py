# Generated by Django 2.1.1 on 2018-11-23 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0007_auto_20181114_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classtoteacher',
            name='stu_class',
            field=models.ForeignKey(limit_choices_to={'school_id__in': ['115']}, on_delete=django.db.models.deletion.CASCADE, related_name='tutor', to='school.StuClass', verbose_name='班级'),
        ),
    ]