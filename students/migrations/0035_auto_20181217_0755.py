# Generated by Django 2.1.1 on 2018-12-17 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0034_auto_20181123_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='chinese_zodiac',
            field=models.IntegerField(blank=True, choices=[(1, '猴'), (2, '鸡'), (3, '狗'), (4, '猪'), (5, '鼠'), (6, '牛'), (7, '虎'), (8, '兔'), (9, '龙'), (10, '蛇'), (11, '马'), (12, '羊')], null=True, verbose_name='生肖'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='constellation',
            field=models.IntegerField(blank=True, choices=[(1, '摩羯'), (2, '水瓶'), (3, '双鱼'), (4, '白羊'), (5, '金牛'), (6, '双子'), (7, '巨蟹'), (8, '狮子'), (9, '处女'), (10, '天秤'), (11, '天蝎'), (12, '射手')], null=True, verbose_name='星座'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='day_age',
            field=models.IntegerField(blank=True, null=True, verbose_name='日龄'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(1, '男'), (2, '女')], null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Grade', verbose_name='年级'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='graduate_institutions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='school.SchoolInfo', verbose_name='毕业园校'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='id_card',
            field=models.CharField(blank=True, db_index=True, max_length=32, null=True, verbose_name='身份证号码'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='period',
            field=models.IntegerField(blank=True, null=True, verbose_name='届别'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='student/photo/', verbose_name='照片'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='residence_city',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='户籍市'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='residence_province',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='户籍省'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='residence_region',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='户籍县区'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='student_code',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='学籍号'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='telephone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='电话号码'),
        ),
    ]
