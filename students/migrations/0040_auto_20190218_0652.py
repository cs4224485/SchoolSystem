# Generated by Django 2.1.1 on 2019-02-18 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0039_auto_20190117_0606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='images',
            new_name='img',
        ),
    ]
