# Generated by Django 2.1.1 on 2018-10-16 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20181015_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentparents',
            name='birthday',
            field=models.DateField(null=True, verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='company',
            field=models.CharField(max_length=64, null=True, verbose_name='工作单位'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='education',
            field=models.IntegerField(choices=[(0, '小学'), (1, '初中'), (2, '高中（中专'), (3, '大专'), (4, '本科'), (5, '硕士'), (6, '博士'), (7, '博士后'), (8, '院士')], null=True, verbose_name='学历'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='first_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='名'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='job',
            field=models.CharField(max_length=32, null=True, verbose_name='职位'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='last_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='姓'),
        ),
        migrations.AlterField(
            model_name='studentparents',
            name='telephone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='联系电话'),
        ),
    ]