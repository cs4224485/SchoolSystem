# Generated by Django 2.1.1 on 2019-02-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0025_familyvisitrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='familyvisitrecord',
            name='state',
            field=models.SmallIntegerField(choices=[(1, '预约中'), (2, '已完成'), (3, '已取消')], default=1, verbose_name='预约状态'),
        ),
        migrations.AlterModelTable(
            name='familyvisitrecord',
            table='FamilyVisitRecord',
        ),
    ]
