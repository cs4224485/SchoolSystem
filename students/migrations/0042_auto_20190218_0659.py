# Generated by Django 2.1.1 on 2019-02-18 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0041_auto_20190218_0656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='picture',
            new_name='images',
        ),
    ]
