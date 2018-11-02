# from django.db import models
#
# # Create your models here.
#
#
# class ChoiceField(models.Model):
#     '''
#     可选择的填表字段
#     '''
#     fieldName = models.CharField(verbose_name='字段名称', max_length=32)
#     field_english = models.CharField(verbose_name='字段英文名', max_length=32)
#     field_type = models.ForeignKey(verbose_name='类型', to='FieldType', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.fieldName
#
#
# class FieldType(models.Model):
#     '''
#     每个字段所属于的表
#     '''
#     name_choice = ((1, '学生信息'), (2, '健康信息'), (3, '家庭信息'), (4, '家长信息'), (5, '自定义信息'))
#     name = models.IntegerField(verbose_name='所属分类', choices=name_choice)
#
#     def __str__(self):
#         return self.get_name_display()
#
#
# class TableSettings(models.Model):
#     '''
#     学生调查表配置
#     '''
#     stat_time = models.DateField(verbose_name='开始日期')
#     end_time = models.DateField(verbose_name='结束日期', null=True)
#     title = models.CharField(verbose_name='名称', max_length=64)
#     school_range = models.ManyToManyField('SchoolInfo', verbose_name='学校范围', related_name='setting')
#     Qrcode = models.CharField(verbose_name='二维码', null=True, max_length=255)
#     fill_range = models.ManyToManyField('ScopeOfFilling', verbose_name='填表范围')
#
#     # choice_field = models.ManyToManyField(to='ChoiceField', verbose_name='选中字段')
#
#     def __str__(self):
#         return self.title
#
#
# class SettingToField(models.Model):
#     setting = models.ForeignKey(verbose_name='设置信息', to='TableSettings', on_delete=models.CASCADE)
#     fields = models.ForeignKey(verbose_name='字段', to='ChoiceField', on_delete=models.CASCADE)
#     order = models.IntegerField(verbose_name='排序')
#
#
# class ScaleSetting(models.Model):
#     '''
#     量表设置相关
#     '''
#     title = models.CharField(verbose_name='量表标题', max_length=64)
#     setting_table = models.ForeignKey(to='TableSettings', verbose_name='对应的表单', on_delete=models.CASCADE, related_name='scale')
#
#
# class ScaleOptionDes(models.Model):
#     '''
#     量表每个分值的描述信息
#     '''
#
#     scale_table = models.ForeignKey(to='ScaleSetting', verbose_name='对应的量表', on_delete=models.CASCADE, related_name='options')
#     des = models.CharField(verbose_name='分值描述信息', max_length=64)
#
#
# class ScaleLineTitle(models.Model):
#     scale_table = models.ForeignKey(to='ScaleSetting', verbose_name='对应的量表', on_delete=models.CASCADE, related_name='line_title')
#     des = models.CharField(verbose_name='量表行标题', max_length=32)
#
#
# class ScopeOfFilling(models.Model):
#     '''
#     填表范围
#     '''
#     range_choice = ((1, '老师'), (2, '家长'), (3, '学生'))
#     name = models.IntegerField(verbose_name='填表范围', choices=range_choice)
#
#     def __str__(self):
#         return self.get_name_display()
#
#
# class TableInfo(models.Model):
#     '''
#     填表后的相关信息
#     '''
#     table = models.ForeignKey(to='TableSettings', verbose_name='对应的表单', on_delete=models.CASCADE, related_name='table_info')
#     finish_time = models.IntegerField(verbose_name='填表完成的时间(以秒为单位)')
#     # student = models.ForeignKey(to=StudentInfo, verbose_name='填表的学生', on_delete=models.CharField, related_name='student')
#     # teacher = models.ForeignKey(to='TeacherInfo', verbose_name='填表老师', on_delete=models.CharField)