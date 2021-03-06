# Generated by Django 2.1.1 on 2018-10-19 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0048_auto_20181019_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuclass',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Grade', verbose_name='年级'),
        ),
        migrations.AlterField(
            model_name='stuclass',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.SchoolInfo', verbose_name='学校'),
        ),
    ]
