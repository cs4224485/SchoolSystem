# Generated by Django 2.1.1 on 2019-03-05 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0038_auto_20190305_0336'),
        ('students', '0043_auto_20190228_0803'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studenttoparents',
            unique_together={('student', 'parents_wxinfo')},
        ),
    ]
