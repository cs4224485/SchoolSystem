# Generated by Django 2.1.1 on 2018-10-29 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0049_auto_20181019_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScaleLineTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.CharField(max_length=32, verbose_name='量表行标题')),
            ],
        ),
        migrations.CreateModel(
            name='ScaleOptionDes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.CharField(max_length=64, verbose_name='分值描述信息')),
            ],
        ),
        migrations.CreateModel(
            name='ScaleSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='量表标题')),
                ('line_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ScaleLineTitle', verbose_name='量表行标题')),
                ('option_des', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.ScaleOptionDes', verbose_name='量表分值描述信息')),
                ('setting_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.SettingToField', verbose_name='对应的表单')),
            ],
        ),
        migrations.AlterField(
            model_name='fieldtype',
            name='name',
            field=models.IntegerField(choices=[(1, '学生信息'), (2, '健康信息'), (3, '家庭信息'), (4, '家长信息'), (5, '自定义信息')], verbose_name='所属分类'),
        ),
        migrations.AlterField(
            model_name='schoolsettings',
            name='end_time',
            field=models.DateField(null=True, verbose_name='结束日期'),
        ),
    ]
