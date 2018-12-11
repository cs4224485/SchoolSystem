# Generated by Django 2.1.1 on 2018-11-30 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0066_auto_20181116_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.SchoolInfo', verbose_name='学校')),
            ],
        ),
    ]
