from school import models
from school.utils.common_utils import generate_qrcode
from weixinApp.models import IndexNotification, WechatUserInfo


class SurveyFormService(object):
    '''
    处理调查表单相关数据操作
    '''

    def __init__(self, data):
        self.data = data

    def create_form(self):
        '''
        创建表单
        :return:
        '''
        # 将学校选中需要填写的字段保存至数据库
        setting_obj = models.TableSettings.objects.create(title=self.data['title'], stat_time=self.data['statTime'],
                                                          end_time=self.data['endTime'])
        school = self.data.get('school')
        fill_range = self.data.get('range')

        # 生成的二维码文件名
        qrfile_name = generate_qrcode(setting_obj.pk)
        models.TableSettings.objects.filter(id=setting_obj.pk).update(Qrcode=qrfile_name)

        # 填表学校
        setting_obj.school_range.add(*school)
        # 填表范围
        setting_obj.fill_range.add(*fill_range)
        # 添加表单与字段的对应
        temp = []
        index = 1
        for field in self.data['choiceFieldId']:
            field_id = field.get('id')
            required = field.get('required')
            obj = models.SettingToField(setting=setting_obj, fields_id=int(field_id), is_required=required, order=index)
            temp.append(obj)
            index += 1
        models.SettingToField.objects.bulk_create(temp)

        # 添加矩阵量表
        for scale_item in self.data.get('scaleTable'):
            # 创建量表对象
            scale_obj = models.ScaleSetting.objects.create(title=scale_item.get('scaleTitle'),
                                                           setting_table=setting_obj)
            # 创建行标题
            for line in scale_item.get('lineTitle'):
                models.ScaleLineTitle.objects.create(des=line.get('text'), scale_table=scale_obj)

            # 创建选项的描述
            for option_des in scale_item.get('scaleDes'):
                models.ScaleOptionDes.objects.create(des=option_des.get('text'), scale_table=scale_obj)

        # 添加单选多选表
        for choice_item in self.data.get('choiceTable'):
            # 创建选择表对象
            obj = models.ChoiceTable.objects.create(title=choice_item.get('title'), setting_table=setting_obj,
                                                    choice_type=choice_item.get('type'))
            # 创建选项的描述
            for op in choice_item.get('optionDes'):
                models.ChoiceOptionsDes.objects.create(des=op.get('contents'), choice_table=obj)
        self.create_wx_notification(fill_range, school, setting_obj)
        return setting_obj

    def create_wx_notification(self, fill_range, school, obj, is_update=False):
        '''
        创建微信小程序的消息通知
        :param fill_range: 填表人
        :param school:
        :param obj:
        :param is_update: 是否是更新
        :return:
        '''
        # 根据填表人过滤相关的微信小程序用户

        # 如果填表人是学生把家长也需要加进去
        if '3' in fill_range:
            fill_range.append(1)
        wx_user_queryset = WechatUserInfo.objects.filter(user_type__in=fill_range, bind_info__school__in=school)
        if is_update:
            target = obj.notification.first()
            if not target:
                target = IndexNotification.objects.create(event=3, content_object=obj)
            target.associated_users.set(wx_user_queryset)
        else:
            target = IndexNotification.objects.create(event=3, content_object=obj)
            target.associated_users.add(*wx_user_queryset)

    def edit_form(self, setting_queryset):
        '''
        编辑表单
        :return:
        '''
        setting_obj = setting_queryset.first()
        school = self.data.get('school')
        fill_range = self.data.get('range')
        # 更新填表学校
        setting_obj.school_range.set(school)
        # 更新填表范围
        setting_obj.fill_range.set(fill_range)
        # 更新设置信息
        setting_queryset.update(title=self.data['title'], stat_time=self.data['statTime'],
                                end_time=self.data['endTime'])
        # 更新选中的字段
        fields = self.data.get('choiceFieldId')
        new_fields = [{'id': int(field.get('id')), 'required': field.get('required')} for field in fields]
        new_fields_ids = [int(field.get('id')) for field in fields]
        old_fields = models.SettingToField.objects.filter(setting=setting_obj).all().distinct().order_by('order')
        old_fields_ids = [item.fields.pk for item in old_fields]
        temp = []
        for field in new_fields:
            field_id = field.get('id')
            required = int(field.get('required'))
            index = new_fields.index(field)
            if field_id not in old_fields_ids:
                obj = models.SettingToField.objects.create(setting=setting_obj, fields_id=int(field_id), order=index,
                                                           is_required=required)
                temp.append(obj)
                temp.append(obj.pk)
            elif index != old_fields_ids.index(field_id):
                models.SettingToField.objects.filter(setting=setting_obj, fields_id=int(field_id)).update(order=index)
            # 更新必填选填
            query = models.SettingToField.objects.filter(fields=field_id)
            obj_required = query.values('is_required').first()
            if required != obj_required.get('is_required'):
                query.update(is_required=required)

        new_fields_ids.extend(temp)
        del_fields = list(set(old_fields_ids).difference(new_fields_ids))
        for item in del_fields:
            models.SettingToField.objects.filter(fields_id=item).delete()

        # 更新量表
        scale_info = self.data.get('scaleTable')
        self.update_scale_table(scale_info, setting_obj)

        # 更新或新增选项表
        choice_info = self.data.get('choiceTable')
        self.update_choice_table(choice_info, setting_obj)
        self.create_wx_notification(fill_range, school, setting_obj, is_update=True)
        return setting_obj

    def update_choice_table(self, choice_info, setting_obj):
        '''
        根据提交的数据更新选项表
        :param choice_info:
        :param setting_obj:
        :return:
        '''

        choice_l = []
        for table_item in choice_info:
            table_id = table_item.get('id')
            table_title = table_item.get('title')
            options = table_item.get('optionDes')
            choice_type = table_item.get('type')
            if not table_id:
                obj = models.ChoiceTable.objects.create(title=table_title, choice_type=choice_type,
                                                        setting_table=setting_obj)
                for op_item in options:
                    models.ChoiceOptionsDes.objects.create(des=op_item.get('contents'), choice_table=obj)
                choice_l.append(obj.pk)
            else:
                choice_l.append(int(table_id))
                old_option = models.ChoiceOptionsDes.objects.filter(choice_table_id=int(table_id)).only('id')
                old_option_ids = [item.pk for item in old_option]
                # 更新或添加选择表中的选项
                new_option_ids = []
                if options:
                    for op in options:
                        option_id = op.get('id')
                        content = op.get('contents')
                        if not option_id:
                            op_obj = models.ChoiceOptionsDes.objects.create(des=content, choice_table_id=int(table_id))
                            new_option_ids.append(op_obj.pk)
                        else:
                            new_option_ids.append(int(option_id))
                            models.ChoiceOptionsDes.objects.filter(id=int(option_id)).update(des=content)
                del_option_ids = list(set(old_option_ids).difference(new_option_ids))
                for item_id in del_option_ids:
                    models.ChoiceOptionsDes.objects.filter(id=item_id).delete()
        old_table = models.ChoiceTable.objects.filter(setting_table=setting_obj).only('id')
        old_table_ids = [item.id for item in old_table]
        del_table_ids = list(set(old_table_ids).difference(choice_l))
        for del_id in del_table_ids:
            models.ChoiceTable.objects.filter(id=del_id).delete()

    def update_scale_table(self, scale_info, setting_obj):
        '''
        根据提交的数据创建或更新矩阵量表信息
        :param scale_info: 量表信息
        :param setting_obj: 表单对象
        :return:
        '''
        scale_l = []
        for scale in scale_info:
            scale_id = scale.get('id')
            scale_title = scale.get('scaleTitle')
            line_title = scale.get('lineTitle')
            scale_des = scale.get('scaleDes')
            if scale_id:
                scale_l.append(int(scale_id))
            if not scale_id:
                # 如果ID不存在代表新创建的表
                scale_obj = models.ScaleSetting.objects.create(title=scale_title, setting_table=setting_obj)
                for line in line_title:
                    models.ScaleLineTitle.objects.create(des=line.get('text'), scale_table=scale_obj)
                for option in scale_des:
                    models.ScaleOptionDes.objects.create(des=option.get('text'), scale_table=scale_obj)

                scale_l.append(scale_obj.pk)
            else:
                models.ScaleSetting.objects.filter(id=int(scale_id)).update(title=scale_title)
                old_line_title = models.ScaleLineTitle.objects.filter(scale_table_id=int(scale_id)).only('id')
                old_line_ids = [line.id for line in old_line_title]
                old_option_des = models.ScaleOptionDes.objects.filter(scale_table_id=int(scale_id)).only('id')
                old_option_ids = [op.id for op in old_option_des]

                new_line_ids = []
                new_option_ids = []
                # 创建或更新行标题
                if line_title:
                    for line in line_title:
                        line_id = line.get('id')
                        content = line.get('text')
                        if not line_id:
                            line_obj = models.ScaleLineTitle.objects.create(des=content, scale_table_id=scale_id)
                            new_line_ids.append(line_obj.pk)
                        else:
                            new_line_ids.append(int(line_id))
                            models.ScaleLineTitle.objects.filter(id=int(line_id)).update(des=content)
                # 删除旧的行标题
                del_line_id = list(set(old_line_ids).difference(new_line_ids))
                for item_id in del_line_id:
                    models.ScaleLineTitle.objects.filter(id=item_id).delete()

                # 创建或更新选项描述
                if scale_des:
                    for option in scale_des:
                        option_id = option.get('id')
                        content = option.get('text')
                        if not option_id:
                            option_obj = models.ScaleOptionDes.objects.create(des=content, scale_table_id=int(scale_id))
                            new_option_ids.append(option_obj.pk)
                        else:
                            new_option_ids.append(int(option_id))
                            models.ScaleOptionDes.objects.filter(id=int(option_id)).update(des=content)
                del_option_id = list(set(old_option_ids).difference(new_option_ids))
                for item_id in del_option_id:
                    models.ScaleOptionDes.objects.filter(id=item_id).delete()

        scale_table = models.ScaleSetting.objects.filter(setting_table=setting_obj).only('id')
        old_scale_ids = [item.id for item in scale_table]
        del_scale_ids = list(set(old_scale_ids).difference(scale_l))
        for item_id in del_scale_ids:
            models.ScaleSetting.objects.filter(id=item_id).delete()
