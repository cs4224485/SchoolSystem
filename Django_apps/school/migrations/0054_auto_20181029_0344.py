# Generated by Django 2.1.1 on 2018-10-29 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0053_auto_20181029_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scalesetting',
            name='setting_table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scale', to='school.SchoolSettings', verbose_name='对应的表单'),
        ),
    ]
