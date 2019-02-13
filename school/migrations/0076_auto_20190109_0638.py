# Generated by Django 2.1.1 on 2019-01-09 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0075_auto_20190109_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxappsettings',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wx_setting', to='school.SchoolInfo', verbose_name='所对应的学校'),
        ),
    ]