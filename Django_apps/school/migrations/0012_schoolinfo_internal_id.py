# Generated by Django 2.1.1 on 2018-10-11 07:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_remove_schoolinfo_internal_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolinfo',
            name='internal_id',
            field=models.CharField(default=uuid.UUID('7c9c847a-963c-4d5d-94a8-2c622cc079a0'), max_length=255, unique=True, verbose_name='学校内部ID'),
        ),
    ]