# Generated by Django 2.1.1 on 2019-04-17 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0054_auto_20190411_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttoparents',
            name='parents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='students.StudentParents', verbose_name='家长ID'),
        ),
    ]