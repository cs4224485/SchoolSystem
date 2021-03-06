# Generated by Django 2.1.1 on 2018-10-11 06:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_auto_20181011_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='internal_id',
            field=models.CharField(default=uuid.UUID('73e424bb-a4cf-4944-8d59-d3450a2e9ac2'), max_length=255, unique=True, verbose_name='学校内部ID'),
        ),
    ]
