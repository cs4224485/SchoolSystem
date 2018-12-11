from django.db import models


# from students.models import StudentInfo

# Create your models here.


class SchoolInfo(models.Model):
    '''
    学校信息表
    '''

    school_name = models.CharField(verbose_name='学校名称', max_length=64, db_index=True)
    English_name = models.CharField(verbose_name='学校英文名称', max_length=64, null=True)
    abbreviation = models.CharField(verbose_name='学校简称', max_length=16, null=True)
    internal_id = models.CharField(verbose_name='学校内部ID', max_length=255, unique=True)
    school_code = models.CharField(verbose_name='学校编码', max_length=64, null=True)
    country = models.CharField(verbose_name='国家', max_length=32, default='中国')
    local_school_name = models.CharField(verbose_name='学校本地名', max_length=64, null=True)
    logo = models.FileField(verbose_name='学校LOGO', upload_to='school/logo/', default='school/logo/default.png',
                            null=True)
    pattern = models.FileField(verbose_name='学校图案', upload_to='school/pattern/', default='school/logo/default.png',
                               null=True)
    website = models.URLField(verbose_name='学校官网', max_length=128, null=True)
    school_type_choice = (('1', '公立'), ('2', '民办'))
    school_type = models.CharField(verbose_name='学校类型', choices=school_type_choice, default=None, null=True, blank=True,
                                   max_length=4)
    school_layer_choice = ((1, '幼儿园'), (2, '小学'), (3, '初中'), (4, '高中阶段'), (5, '九年一惯制'), (6, '中等职业学校'), (7, '十二年一贯制'))
    school_layer = models.IntegerField(verbose_name='学校层级', choices=school_layer_choice, default=None, null=True,
                                       blank=True)
    create_time = models.DateField(verbose_name='创办时间', null=True)
    province = models.CharField(verbose_name='所在省', max_length=32)
    city = models.CharField(verbose_name='所在市', max_length=32)
    region = models.CharField(verbose_name='所在区县', max_length=32)
    street = models.CharField(verbose_name='所在街道办,乡镇', max_length=32, null=True)
    community = models.ForeignKey(verbose_name='所在居委会', to='Community', on_delete=models.Model, null=True)
    address = models.CharField(verbose_name='校址', max_length=128)
    main_campus_type = ((1, '本部'), (2, '分校或校区'))
    main_campus = models.IntegerField(verbose_name='是本部还是校区', choices=main_campus_type, default=None, null=True)
    campus_district = models.CharField(verbose_name='校区名称', max_length=32, null=True, blank=True)
    campus_english_name = models.CharField(verbose_name='校区英文名', max_length=32, null=True, blank=True)
    competent_organization = models.ManyToManyField('CompetentOrganization', verbose_name='主管单位')
    major = models.ManyToManyField('Major', verbose_name='开设课程')
    group = models.ForeignKey('Group', verbose_name='教育集团', null=True, on_delete=models.CASCADE)
    system = models.ForeignKey('System', verbose_name='办学系统', null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.campus_district:
            return self.school_name + self.campus_district
        else:
            return self.school_name


class Grade(models.Model):
    grade_choice = ((1, '一年级'), (2, '二年级'), (3, '三年级'), (4, '四年级'), (5, '五年级'), (6, '六年级'), (7, '初一'), (8, '初二')
                    , (9, '初三'), (10, '高一'), (11, '高二'), (12, '高三'), (13, '小班'), (14, '中班'), (15, '大班'))
    grade_name = models.IntegerField(choices=grade_choice, unique=True)

    def __str__(self):
        return self.get_grade_name_display()


class StuClass(models.Model):
    '''
    学生班级表
    '''
    grade = models.ForeignKey(verbose_name='年级', to=Grade, on_delete=models.CASCADE)
    school = models.ForeignKey(verbose_name='学校', to=SchoolInfo, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='班级名称', max_length=64)

    def __str__(self):
        return "%s%s" % (self.grade, self.name)

    class Meta:
        unique_together = (("grade", "school", 'name'),)


class Community(models.Model):
    '''
    居委会信息表
    '''
    title = models.CharField(verbose_name='居委会', max_length=32)


class System(models.Model):
    '''
    办学系统信息
    如 西安交大附属中学、西安交大附属小学…
    '''
    title = models.CharField(verbose_name='系统名称', max_length=32)


class Group(models.Model):
    '''
    教育集团信息
    如 打一小学教育集团
    '''
    title = models.CharField(verbose_name='集团名称', max_length=32)


class CompetentOrganization(models.Model):
    '''
    主管部门暂未使用
    '''
    title = models.CharField(verbose_name='主管部门', max_length=32)


class Major(models.Model):
    '''
    学校开设的专业
    '''

    title = models.CharField(verbose_name='专业名称', max_length=16)


class SchoolHonor(models.Model):
    '''
    学校荣誉
    如“中国小学500强（2013）”
    '''

    title = models.CharField(verbose_name='荣誉名称', max_length=32)
    assessment = models.ForeignKey(verbose_name='评测机构', to='Assessment', on_delete=models.CASCADE)


class Assessment(models.Model):
    '''
    荣誉评测机构信息
    '''

    name = models.CharField(verbose_name='机构名称', max_length=32)


class SchoolToHonor(models.Model):
    '''
    学校与荣誉对应表
    '''

    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)
    honor = models.ForeignKey(verbose_name='荣誉', to='SchoolHonor', on_delete=models.CASCADE)
    time = models.DateField(verbose_name='获取时间')


class SchoolTitle(models.Model):
    '''
    学校称号
    如“2018年全国青少年校园网球特色学校”
    '''

    name = models.CharField(verbose_name='称号名称', max_length=32)


class SchoolToTitle(models.Model):
    '''
    学校与称号映射表
    '''
    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)
    title = models.ForeignKey(verbose_name='称号', to='SchoolTitle', on_delete=models.CASCADE)
    time = models.DateField(verbose_name='获取时间')


class ScoreLine(models.Model):
    '''
    学校历年录取分数线表
    '''

    line = models.IntegerField(verbose_name='分数线')
    year_choice = []
    import datetime
    for r in range(2010, (datetime.datetime.now().year + 1)):
        year_choice.append((r, r))
    Year = models.IntegerField(verbose_name='年度', choices=year_choice)
    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)


class SchoolBoundary(models.Model):
    '''
    学校学区范围
    '''
    stage_choice = ((1, '幼儿园'), (2, '小学'), (3, '初高中'))
    import datetime
    year_choice = []
    for r in range(2010, (datetime.datetime.now().year + 1)):
        year_choice.append((r, r))
    Year = models.IntegerField(verbose_name='年度', choices=year_choice)
    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)


class SchoolHistory(models.Model):
    '''
    学校历史信息
    '''
    action_choice = ((1, '改名'), (2, '搬迁'), (3, '拆分'), (4, '合并'))
    action = models.IntegerField(verbose_name='记录类型', choices=action_choice)
    start_time = models.DateField(verbose_name='开始日期')
    end_time = models.DateField(verbose_name='结束日期')
    old_name = models.CharField(verbose_name='学校源名称', max_length=64)
    new_name = models.CharField(verbose_name='学校新名称', max_length=64)
    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)


class SchoolCalendar(models.Model):
    '''
    学校校历信息
    '''

    school = models.ForeignKey(verbose_name='学校', to='SchoolInfo', on_delete=models.CASCADE)
    des_choice = ((1, '开学'), (2, '寒假'), (4, '暑假'), (3, '校动会'), (5, '期中考试'), (6, '期末考试'), (7, '校庆'), (8, '毕业典礼'))
    date_des = models.IntegerField(verbose_name='日期描述', choices=des_choice)
    date = models.DateField(verbose_name='日期')
    end_date = models.DateField(verbose_name="结束日期", null=True, blank=True)


class Course(models.Model):
    '''
    课程信息
    '''
    course_des = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.course_des


class SchoolTimetable(models.Model):
    '''
    学校课程表
    '''
    stu_class = models.ForeignKey(to='StuClass', verbose_name='班级', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(to='Course', verbose_name='课程', on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(to='teacher.TeacherInfo', verbose_name='代课老师', on_delete=models.CASCADE, blank=True, null=True)
    week_choice = ((1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'))
    week = models.SmallIntegerField(choices=week_choice, verbose_name='星期', blank=True, null=True)
    time_range = models.TimeField(verbose_name='时间段')
    single_double_week_choice = ((1, '单'), (2, '双'))
    single_double_week = models.SmallIntegerField(verbose_name='课程单双周',  choices=single_double_week_choice, null=True, blank=True)
    other_event_choice = ((1, '课间操'), (2, '午休'))
    school = models.ForeignKey(to='SchoolInfo', verbose_name='学校', on_delete=models.CASCADE)
    other_event = models.SmallIntegerField(choices=other_event_choice, verbose_name='学校其他事件', null=True, blank=True)
    info_type_choice = ((1, '课程'), (2, '其他事件'))
    info_type = models.SmallIntegerField(choices=info_type_choice, verbose_name='存储的类型', default=1)

    def __str__(self):
        return '%s:%s:%s' %(self.stu_class.name, self.teacher.last_name+self.teacher.first_name, self.course.course_des)

# ------------------------- 表单设置相关表  ---------------------------------


class ChoiceField(models.Model):
    '''
    可选择的填表字段
    '''
    fieldName = models.CharField(verbose_name='字段名称', max_length=32)
    field_english = models.CharField(verbose_name='字段英文名', max_length=32)
    field_type = models.ForeignKey(verbose_name='类型', to='FieldType', on_delete=models.CASCADE)

    def __str__(self):
        return self.fieldName


class FieldType(models.Model):
    '''
    每个字段所属于的表
    '''
    name_choice = ((1, '学生信息'), (2, '健康信息'), (3, '家庭信息'), (4, '家长信息'), (5, '自定义信息'))
    name = models.IntegerField(verbose_name='所属分类', choices=name_choice)

    def __str__(self):
        return self.get_name_display()


class TableSettings(models.Model):
    '''
    学生调查表配置
    '''
    stat_time = models.DateField(verbose_name='开始日期')
    end_time = models.DateField(verbose_name='结束日期', null=True)
    title = models.CharField(verbose_name='名称', max_length=64)
    school_range = models.ManyToManyField('SchoolInfo', verbose_name='学校范围', related_name='setting')
    Qrcode = models.CharField(verbose_name='二维码', null=True, max_length=255)
    fill_range = models.ManyToManyField('ScopeOfFilling', verbose_name='填表范围')

    # choice_field = models.ManyToManyField(to='ChoiceField', verbose_name='选中字段')

    def __str__(self):
        return self.title


class SettingToField(models.Model):
    '''
    表单选中的字段
    '''
    setting = models.ForeignKey(verbose_name='设置信息', to='TableSettings', on_delete=models.CASCADE)
    fields = models.ForeignKey(verbose_name='字段', to='ChoiceField', on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name='排序')

    class Meta:
        unique_together = (('setting', 'fields'),)


class ScaleSetting(models.Model):
    '''
    量表设置相关
    '''
    title = models.CharField(verbose_name='量表标题', max_length=64)
    setting_table = models.ForeignKey(to='TableSettings', verbose_name='对应的表单', on_delete=models.CASCADE,
                                      related_name='scale')

    def __str__(self):
        return self.title


class ScaleOptionDes(models.Model):
    '''
    量表每个分值的描述信息
    '''

    scale_table = models.ForeignKey(to='ScaleSetting', verbose_name='对应的量表', on_delete=models.CASCADE,
                                    related_name='options')
    des = models.CharField(verbose_name='分值描述信息', max_length=64)

    def __str__(self):
        return self.des


class ScaleLineTitle(models.Model):
    '''
    量表行标题信息
    '''
    scale_table = models.ForeignKey(to='ScaleSetting', verbose_name='对应的量表', on_delete=models.CASCADE,
                                    related_name='line_title')
    des = models.CharField(verbose_name='量表行标题', max_length=64)


class ChoiceTable(models.Model):
    '''
    单选和多选类型设置信息
    '''
    title = models.CharField(verbose_name='标题', max_length=64)
    setting_table = models.ForeignKey(to='TableSettings', verbose_name='对应的表单', on_delete=models.CASCADE,
                                      related_name='choice')
    choice_type_choice = ((1, '单选'), (2, '多选'))
    choice_type = models.PositiveIntegerField(verbose_name='单选或多选', choices=choice_type_choice)

    def __str__(self):
        return self.title


class ChoiceOptionsDes(models.Model):
    des = models.CharField(verbose_name='每个选项的描述', max_length=64)
    choice_table = models.ForeignKey(to='ChoiceTable', verbose_name='对应的选择表', on_delete=models.CASCADE,
                                     related_name='opdes')

    def __str__(self):
        return self.des


class ScopeOfFilling(models.Model):
    '''
    填表范围
    '''

    range_choice = ((1, '老师'), (2, '家长'), (3, '学生'))
    name = models.IntegerField(verbose_name='填表范围', choices=range_choice)

    def __str__(self):
        return self.get_name_display()


class TableInfo(models.Model):
    '''
    填表后的相关信息
    '''
    table = models.ForeignKey(to='TableSettings', verbose_name='对应的表单', on_delete=models.CASCADE,
                              related_name='table_info')
    finish_time = models.IntegerField(verbose_name='填表完成的时间(以秒为单位)')
    student = models.ForeignKey("students.StudentInfo", verbose_name='填表的学生', on_delete=models.CharField,
                                related_name='for_student')
    # teacher = models.ForeignKey(to='TeacherInfo', verbose_name='填表老师', on_delete=models.CharField)
