# Generated by Django 2.1.1 on 2019-04-23 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0088_auto_20190423_1358'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='choicefield',
            table='ChoiceField',
        ),
        migrations.AlterModelTable(
            name='choiceoptionsdes',
            table='ChoiceOptionsDes',
        ),
        migrations.AlterModelTable(
            name='choicetable',
            table='ChoiceTable',
        ),
        migrations.AlterModelTable(
            name='fieldtype',
            table='FieldType',
        ),
        migrations.AlterModelTable(
            name='scalelinetitle',
            table='ScaleLineTitle',
        ),
        migrations.AlterModelTable(
            name='scaleoptiondes',
            table='ScaleOptionDes',
        ),
        migrations.AlterModelTable(
            name='scalesetting',
            table='ScaleSetting',
        ),
        migrations.AlterModelTable(
            name='scopeoffilling',
            table='ScopeOfFilling',
        ),
        migrations.AlterModelTable(
            name='settingtofield',
            table='SettingToField',
        ),
        migrations.AlterModelTable(
            name='tableinfo',
            table='TableInfo',
        ),
        migrations.AlterModelTable(
            name='tablesettings',
            table='TableSettings',
        ),
        migrations.AlterModelTable(
            name='wxappsettings',
            table='WXappSettings',
        ),
    ]
