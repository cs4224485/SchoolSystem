# Generated by Django 2.2.1 on 2019-10-12 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudentMentalHealth', '0007_performance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='options',
            new_name='option',
        ),
    ]