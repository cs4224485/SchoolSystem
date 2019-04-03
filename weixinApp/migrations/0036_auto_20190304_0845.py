# Generated by Django 2.1.1 on 2019-03-04 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weixinApp', '0035_auto_20190304_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emblem',
            name='custom_name',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='自定义名称'),
        ),
        migrations.AlterField(
            model_name='emblem',
            name='emblem_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixinApp.EmblemType', verbose_name='徽章类型'),
        ),
    ]