# Generated by Django 2.1.1 on 2018-11-22 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0066_auto_20181116_0759'),
        ('students', '0032_choicequestion'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='choicequestion',
            unique_together={('student', 'choice_table')},
        ),
        migrations.AlterUniqueTogether(
            name='scalequestion',
            unique_together={('student', 'scale')},
        ),
    ]
