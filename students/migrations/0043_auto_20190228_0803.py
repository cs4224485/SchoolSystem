# Generated by Django 2.1.1 on 2019-02-28 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0042_auto_20190218_0659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='images',
            new_name='img',
        ),
    ]
