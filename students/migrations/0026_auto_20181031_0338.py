# Generated by Django 2.1.1 on 2018-10-31 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0025_auto_20181030_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='student_code',
            field=models.CharField(max_length=64, null=True, verbose_name='学籍号'),
        ),
    ]
