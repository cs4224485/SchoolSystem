# Generated by Django 2.1.1 on 2018-12-20 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0037_auto_20181220_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttoparents',
            name='parents',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.StudentParents', verbose_name='家长ID'),
        ),
        migrations.AlterField(
            model_name='studenttoparents',
            name='parents_wxinfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weixinApp.WechatUserInfo', verbose_name='家长的微信信息'),
        ),
    ]
