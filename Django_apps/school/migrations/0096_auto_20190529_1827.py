# Generated by Django 2.1.1 on 2019-05-29 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0095_auto_20190513_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableinfo',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]