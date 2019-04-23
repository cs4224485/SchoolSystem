from django.db import models
from school.models import SchoolInfo, Grade, StuClass, ScaleSetting, ScaleLineTitle, ScaleOptionDes
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.


class StudentInfo(models.Model):
    '''
    学生基本信息表
    '''
    interior_student_id = models.CharField(verbose_name='内部学生ID', unique=True, max_length=255, null=True)
    first_name = models.CharField(verbose_name='学生名', max_length=128)
    last_name = models.CharField(verbose_name='学生姓', max_length=128)
    full_name = models.CharField(verbose_name='学生全名', db_index=True, max_length=256)
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.IntegerField(choices=gender_choice, verbose_name='性别', default=None, null=True, blank=True)
    country = models.ForeignKey('Country', verbose_name='国籍', on_delete=models.CASCADE, default=1)
    nation = models.CharField(verbose_name='民族', max_length=32, null=True, default='汉族')
    residence_province = models.CharField(verbose_name='户籍省', max_length=16, null=True, blank=True)
    residence_city = models.CharField(verbose_name='户籍市', max_length=16, null=True, blank=True)
    residence_region = models.CharField(verbose_name='户籍县区', max_length=16, null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    day_age = models.IntegerField(verbose_name='日龄', null=True, blank=True)
    constellation_choice = (
        (1, "摩羯"), (2, "水瓶"), (3, "双鱼"), (4, "白羊"), (5, "金牛"), (6, "双子"), (7, "巨蟹"), (8, "狮子"), (9, "处女"), (10, "天秤"),
        (11, "天蝎"), (12, "射手"))
    constellation = models.IntegerField(verbose_name='星座', choices=constellation_choice, null=True, blank=True)
    chinese_zodiac_choice = ((1, '猴'), (2, '鸡'), (3, '狗'), (4, '猪'), (5, '鼠'),
                             (6, '牛'), (7, '虎'), (8, '兔'), (9, '龙'), (10, '蛇'), (11, '马'), (12, '羊'))
    id_card = models.CharField(verbose_name='身份证号码', null=True, db_index=True, max_length=32, blank=True)
    student_code = models.CharField(verbose_name='学籍号', null=True, max_length=64, blank=True)
    telephone = models.CharField(verbose_name='电话号码', max_length=32, null=True, blank=True)
    chinese_zodiac = models.IntegerField(verbose_name='生肖', choices=chinese_zodiac_choice, null=True, blank=True)
    photo = models.FileField(upload_to='student/photo/', verbose_name='照片', null=True, blank=True)
    email = models.EmailField(verbose_name='邮箱', null=True, unique=True, blank=True)
    QQ = models.IntegerField(verbose_name='QQ', null=True, unique=True, blank=True)
    wechat = models.CharField(verbose_name='微信', null=True, max_length=32, blank=True)
    create_time = models.DateField(verbose_name='创建日期', auto_now=True)
    period = models.IntegerField(verbose_name='届别', null=True, blank=True)
    grade = models.ForeignKey(verbose_name='年级', to=Grade, on_delete=models.CASCADE, null=True, blank=True)
    graduate_institutions = models.ForeignKey(to=SchoolInfo, verbose_name='毕业园校', on_delete=models.CASCADE, null=True,
                                              related_name='school', blank=True)
    school = models.ForeignKey(verbose_name='所在学校', to=SchoolInfo, on_delete=models.CASCADE)
    stu_class = models.ForeignKey(verbose_name='所在班级', to=StuClass, on_delete=models.CASCADE, null=True,
                                  related_name='student_class')

    def __str__(self):
        return self.full_name


class GraduateInstitutions(models.Model):
    '''
    毕业机构表
    '''

    name = models.CharField(verbose_name='学校名称', max_length=32, )

    def __str__(self):
        return self.name


class Country(models.Model):
    '''
    国籍信息表
    '''
    country_name = models.CharField(verbose_name='国籍', max_length=32)
    english_name = models.CharField(verbose_name='english', max_length=32)
    img = models.FileField(upload_to='country_img')

    def __str__(self):
        return self.country_name


class HealthInfo(models.Model):
    '''
    健康信息表
    '''
    disability_choice = ((1, '无'), (2, '视力'), (3, '听力语言'), (4, '智力'), (5, '肢体'), (6, '精神'))
    disability = models.IntegerField(verbose_name='残疾', choices=disability_choice, default=1, null=True)
    blood_type_choice = ((1, 'A'), (2, 'B'), (3, 'O'), (4, 'AB'), (5, '不知道'))
    blood_type = models.IntegerField(verbose_name='血型', choices=blood_type_choice, null=True, blank=True)
    student = models.ForeignKey('StudentInfo', on_delete=models.CASCADE, unique=True, db_index=True)
    allergy = models.ForeignKey('Allergy', verbose_name='过敏源', on_delete=models.CASCADE, null=True)
    InheritedDisease = models.ForeignKey('InheritedDisease', verbose_name='遗传病', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.student.first_name + "健康信息"


class HealthRecord(models.Model):
    '''
    健康信息记录
    '''
    height = models.IntegerField(verbose_name='身高', null=True, blank=True)
    weight = models.DecimalField(verbose_name='体重', max_digits=4, decimal_places=2, null=True, blank=True)
    vision_left = models.DecimalField(verbose_name='左眼视力', max_digits=3, decimal_places=2, null=True, blank=True)
    vision_right = models.DecimalField(verbose_name='右眼视力', max_digits=3, decimal_places=2, null=True, blank=True)
    vision_status_choice = ((1, '正常'), (2, '远视'), (3, '近视'), (4, '散光'), (5, '其他'))
    vision_status = models.IntegerField(verbose_name='视力情况', null=True)
    record_date = models.DateField(verbose_name='记录日期', auto_now=True)
    health_info = models.ForeignKey(to='HealthInfo', verbose_name='健康信息', on_delete=models.CASCADE, related_name='record')
    measure_type_choice = ((1, '校测'), (2, '自测'))
    measure_type = models.IntegerField(verbose_name='测试类型', default=1, choices=measure_type_choice, null=True, blank=True)


class Allergy(models.Model):
    '''
    过敏源表
    '''
    title = models.CharField(max_length=64, verbose_name='过敏源')

    def __str__(self):
        return self.title


class InheritedDisease(models.Model):
    '''
    遗传病表
    '''
    title = models.CharField(max_length=64, verbose_name='遗传病')

    def __str__(self):
        return self.title


class FamilyInfo(models.Model):
    '''
    家庭信息表
    '''
    living_condition_choice = ((1, '一居室'), (2, '二居室'), (3, '三居室'), (4, '三居以上'))
    living_condition = models.IntegerField(verbose_name='居住条件', choices=living_condition_choice, null=True, blank=True)
    living_type_choice = ((1, '自有'), (2, '租赁'), (3, '亲友住宅'))
    living_type = models.IntegerField(verbose_name='居住类型', choices=living_condition_choice, null=True, blank=True)
    language_choice = ((1, '中文普通话'), (2, '中文方言'), (3, '英语'), (4, '其他外语'))
    language = models.IntegerField(verbose_name='家庭语言', choices=language_choice, default=1, null=True, blank=True)
    create_time = models.DateField(verbose_name='创建日期', auto_now=True)
    # member_of_family = models.ManyToManyField('FamilyMember', verbose_name='家庭成员', blank=True)
    family_status = models.ManyToManyField('FamilyStatus', verbose_name='家庭状况', blank=True, null=True)
    student = models.ForeignKey('StudentInfo', verbose_name='学生', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.full_name + "家庭信息"


class FamilyMember(models.Model):
    '''
    家庭成员信息表，暂未使用
    '''
    relations = models.CharField(verbose_name='家庭关系', max_length=16)
    Is_living = models.BooleanField(verbose_name='是否共同居住')
    handle_shuttle = models.BooleanField(verbose_name='是否为主要接送人')


class FamilyStatus(models.Model):
    '''
    家庭状况表
    '''
    status_choice = ((1, '再婚'), (2, '离异'), (3, '留守'), (4, '领养'), (5, '单亲'), (6, '其他'))
    status = models.IntegerField(verbose_name='家庭状况', choices=status_choice)

    def __str__(self):
        return self.get_status_display()


class HomeAddress(models.Model):
    '''
    家庭住址表
    '''
    province = models.CharField(verbose_name='省', max_length=16, null=True, blank=True)
    city = models.CharField(verbose_name='市', max_length=16, null=True, blank=True)
    region = models.CharField(verbose_name='区县', max_length=16, null=True, blank=True)
    address = models.CharField(verbose_name='详细地址', max_length=128, null=True, blank=True)
    record_time = models.DateField(verbose_name='日期', auto_now=True)
    family = models.ForeignKey('FamilyInfo', verbose_name='家庭', on_delete=models.CASCADE)


class StudentParents(models.Model):
    '''
    学生家长信息表
    '''
    first_name = models.CharField(verbose_name='名', max_length=64, null=True, blank=True)
    last_name = models.CharField(verbose_name='姓', max_length=64, null=True, blank=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    telephone = models.CharField(verbose_name='联系电话', max_length=32, null=True, blank=True)
    education_choice = ((1, '博士'), (2, '硕士'), (3, '本科'), (4, '大专'), (5, '高中'), (6, '高中以下'), (7, '暂不知道'))
    education = models.IntegerField(verbose_name='学历', choices=education_choice, null=True, blank=True)
    company = models.CharField(verbose_name='工作单位', max_length=64, null=True, blank=True)
    job = models.CharField(verbose_name='职位', max_length=32, null=True, blank=True)
    wechat = models.CharField(verbose_name='微信', max_length=32, null=True, blank=True)
    wx_info = GenericRelation(to='weixinApp.WechatUserInfo')
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.IntegerField(choices=gender_choice, verbose_name='性别', default=None, null=True, blank=True)

    def __str__(self):
        return self.first_name + self.last_name


class StudentToParents(models.Model):
    '''
    学生与家长关系映射表
    '''

    student = models.ForeignKey(verbose_name='学生ID', to='StudentInfo', on_delete=models.CASCADE, related_name='student')
    parents_wxinfo = models.ForeignKey(verbose_name='家长的微信信息', to='weixinApp.WechatUserInfo', on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='stu_parent')
    parents = models.ForeignKey(verbose_name='家长ID', to='StudentParents', on_delete=models.CASCADE, null=True,
                                blank=True, related_name='parent')
    relation_choice = ((1, '父亲'), (2, '母亲'), (3, '爷爷'), (4, '奶奶'), (5, '外公'), (6, '外婆'), (7, '其他长辈'), (8, '其他平辈'))
    relation = models.IntegerField(verbose_name='与学生关系', choices=relation_choice)
    is_main_contact = models.BooleanField(verbose_name='是否为主要接送人', null=True, blank=True)

    def __str__(self):
        if self.parents:
            return "学生：%s 家长：%s" % (self.student.full_name, self.parents.last_name + self.parents.first_name)
        else:
            return "学生：%s 家长微信：%s" % (self.student.full_name, self.parents_wxinfo)

    class Meta:
        unique_together = (('student', 'parents_wxinfo'),)


class ScaleQuestion(models.Model):
    '''
    矩阵量表信息与学生对应表
    '''
    student = models.ForeignKey(verbose_name='对应学生', to=StudentInfo, on_delete=models.CASCADE)
    scale = models.ForeignKey(verbose_name='对应量表', to=ScaleSetting, on_delete=models.CASCADE)

    # question = models.ForeignKey(verbose_name='对应的自定制问题表', to='CustomizationQuestion', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'scale'),)

    def __str__(self):
        return '%s:%s' % (self.student.full_name, self.scale.title)


class ScaleValue(models.Model):
    '''
    量表的行标题所对应的值
    '''
    title = models.ForeignKey(verbose_name='对应的行标题', to=ScaleLineTitle, on_delete=models.CASCADE)
    value = models.ForeignKey(verbose_name='对应的值', to=ScaleOptionDes, on_delete=models.CASCADE)
    scale_stu = models.ForeignKey(verbose_name='对相应的学生量表', to='ScaleQuestion', on_delete=models.CASCADE,
                                  related_name='scale_value')


class ChoiceQuestion(models.Model):
    '''
    学生填写选择表的信息
    '''

    student = models.ForeignKey(verbose_name='对应学生', to=StudentInfo, on_delete=models.CASCADE)
    choice_table = models.ForeignKey(verbose_name='对应的选项表', to='school.ChoiceTable', on_delete=models.CASCADE)
    values = models.ManyToManyField(verbose_name='对应选择的值', to='school.ChoiceOptionsDes')

    class Meta:
        unique_together = (('student', 'choice_table'),)

    def __str__(self):
        return '%s:%s' % (self.student.full_name, self.choice_table.title)
