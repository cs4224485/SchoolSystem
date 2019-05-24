# Generated by Django 2.1.1 on 2018-12-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_remove_teacherinfo_wechat_open_id'),
        ('students', '0035_auto_20181217_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentparents',
            name='wechat_open_id',
        ),
        migrations.AlterField(
            model_name='studenttoparents',
            name='relation',
            field=models.IntegerField(choices=[(1, '父亲'), (2, '母亲'), (3, '爷爷'), (4, '奶奶'), (5, '外公'), (6, '外婆'), (7, '其他长辈'), (8, '其他平辈')], verbose_name='与学生关系'),
        ),
        migrations.DeleteModel(
            name='WechatOpenID',
        ),
    ]