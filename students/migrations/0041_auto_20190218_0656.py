# Generated by Django 2.1.1 on 2019-02-18 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0040_auto_20190218_0652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='img',
            new_name='picture',
        ),
    ]
