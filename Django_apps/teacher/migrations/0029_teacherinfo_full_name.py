# Generated by Django 2.1.1 on 2019-02-21 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0028_auto_20190219_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherinfo',
            name='full_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='教师全名'),
        ),
    ]