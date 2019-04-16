# Generated by Django 2.1.1 on 2019-04-11 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0053_auto_20190409_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthrecord',
            name='health_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='students.HealthInfo', verbose_name='健康信息'),
        ),
    ]
