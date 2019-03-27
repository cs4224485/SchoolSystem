from rest_framework.views import APIView, Response
from weixinApp.service.user_service import *
from weixinApp import models
from school import models as scmodels
from weixinApp.auth.auth import WeiXinAuth
from weixinApp.service.decorator import *
from django.utils.decorators import method_decorator
from weixinApp.serialize.person_center import StudentSerialize


class BindUser(APIView):
    '''
    授权获取openid绑定到小程序
    '''

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            code = request.data.get('code')
            if not code:
                res.code = -1
                res.msg = '未能获取到code值'
                return Response(res.get_dict)
            open_id = UserService.getWeChatOpenId(code)
            if not open_id:
                res.code = -1
                res.msg = '获取openid失败'
                return Response(res.get_dict)
            user_bind_info = models.WechatBindInfo.objects.filter(open_id=open_id, school_id=settings.SCHOOL_ID).first()
            if not user_bind_info:
                salt = UserService.geneSalt()
                user_bind_info = models.WechatBindInfo.objects.create(open_id=open_id, school_id=settings.SCHOOL_ID,
                                                                      salt=salt)
            if user_bind_info:
                user_info = models.WechatUserInfo.objects.filter(bind_info=user_bind_info).first()
                token = "%s#%s" % (UserService.geneAuthCode(user_bind_info), user_bind_info.id)
                res_data = {'token': token, 'identity': ""}
                if user_info:
                    identity = user_info.user_type
                    res_data['identity'] = identity
                res.code = 200
                res.data = res_data
                res.msg = '绑定成功'
            else:
                raise Exception
        except Exception as e:
            res.code = -1
            res.msg = '绑定失败'
        return Response(res.get_dict)


class BindChildren(APIView):
    '''
    家长绑定学生
    '''
    authentication_classes = [WeiXinAuth]

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            first_name = request.data.get('firstname')
            last_name = request.data.get('lastname')
            relation = request.data.get('relation')
            stu_class = request.data.get('_class')
            nickname = request.data.get('nickname', '')
            avatar = request.data.get('avatar', '')

            if not first_name:
                res.code = -1
                res.msg = '请输入名'
                return Response(res.get_dict)

            if not last_name:
                res.code = -1
                res.msg = '请输入姓'
                return Response(res.get_dict)

            if not stu_class:
                res.code = -1
                res.msg = "请选择所在班级"
                return Response(res.get_dict)

            student_obj = stumodels.StudentInfo.objects.filter(first_name=first_name,
                                                               last_name=last_name,
                                                               stu_class_id=stu_class,
                                                               school_id=settings.SCHOOL_ID).first()
            if not student_obj:
                res.code = -1
                res.msg = "家长您好，请确定您的孩子在我校就读。"
                return Response(res.get_dict)

            if not relation:
                res.code = -1
                res.msg = '请选择与学生的关系'
                return Response(res.get_dict)
            # 获取用户微信绑定信息
            bind_info = models.WechatBindInfo.objects.filter(open_id=request.user).first()

            # 如果用户微信详细信息存在就更新不存在就创建
            user_info, state = models.WechatUserInfo.objects.update_or_create(user_type=1, bind_info=bind_info,
                                                                              defaults={'bind_info': bind_info,
                                                                                        'nickname': nickname,
                                                                                        'avatar': avatar})
            parent_to_children_obj = stumodels.StudentToParents.objects.filter(student=student_obj,
                                                                               relation=relation).first()
            # 判断之前的绑定信息是否存在
            if parent_to_children_obj:
                parents_obj = parent_to_children_obj.parents
                # 如果有绑定信息但是没有家长的微信账号信息那么仅更新微信信息
                if parents_obj:
                    user_info.content_object = parents_obj
                    parent_to_children_obj.parents_wxinfo = user_info
                    user_info.save()
                    parent_to_children_obj.save()
                # 如果没用家长信息则表示该学生已被绑定（注意：此时没有家长的详细信息）
                elif parent_to_children_obj.parents_wxinfo:
                    res.code = -1
                    res.msg = '该学生已被绑定'
                    return Response(res.get_dict)
            else:
                stumodels.StudentToParents.objects.update_or_create(parents_wxinfo=user_info, student=student_obj,
                                                                    defaults={"relation": relation})
            res.code = 200
            res.msg = '绑定成功'
            res.data = {'identity': 1}
        except Exception as e:
            print(e)
            res.code = -1
            res.msg = '绑定失败'
        return Response(res.get_dict)


class FilterClass(APIView):
    '''
    根据年级过滤班级
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            grade = int(request.GET.get('grade', 0))
            if not grade:
                res.code = -1
                res.msg = '请提供年级信息'
                return Response(res.get_dict)

            grade_obj = scmodels.Grade.objects.filter(grade_name=grade).first()
            if not grade_obj:
                res.code = -1
                res.msg = '该年级不存在'
                return Response(res.get_dict)
            class_queryset = scmodels.StuClass.objects.filter(grade=grade_obj, school_id=settings.SCHOOL_ID)
            if not class_queryset:
                raise Exception
            class_list = []
            for item in class_queryset:
                class_list.append({'id': item.id, 'name': item.name})
            res.state = True
            res.code = 200
            res.data = class_list
        except Exception as e:
            print(e)
            res.code = -1
            res.msg = '获取到班级信息失败'
        return Response(res.get_dict)


class PersonCenter(APIView):
    '''
    个人中心接口
    '''
    authentication_classes = [WeiXinAuth]

    @method_decorator(get_user_obj)
    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            obj = kwargs.get('obj')
            if not obj:
                res.code = -1
                res.msg = '获取身份信息异常'
                return Response(res.get_dict)
            data_info = None
            if isinstance(obj, stumodels.StudentToParents):
                student_obj = obj.student
                data_info = StudentSerialize(student_obj)

            if not data_info:
                res.code = -1
                res.msg = '获取信息失败'
                return Response(res.get_dict)

            res.data = {'info': data_info.data}
            res.code = 200
            res.state = True
        except Exception as e:
            res.code = -1
            res.msg = '获取信息失败'
        return Response(res.get_dict)