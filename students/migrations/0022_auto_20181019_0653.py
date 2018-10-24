# Generated by Django 2.1.1 on 2018-10-19 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0021_auto_20181019_0609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='school',
        ),
        migrations.RemoveField(
            model_name='stuclass',
            name='school',
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Grade', verbose_name='年级'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='stu_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.StuClass', verbose_name='所在班级'),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='StuClass',
        ),
    ]
