# Generated by Django 2.1.1 on 2019-05-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0057_auto_20190507_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentparents',
            name='occupation',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='职业'),
        ),
    ]