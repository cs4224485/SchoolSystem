# Author: harry.cai
# DATE: 2018/9/16
import functools
from django.urls import re_path, reverse
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.db.models import Q, ManyToManyField, ForeignKey
from django.http import QueryDict
from django import forms
from stark.utils.page import Pagination
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple


class ModelConfigMapping(object):
    '''
    封装注册相关信息
    '''

    def __init__(self, model, config, prev):
        self.model = model
        self.config = config
        self.prev = prev


class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            if isinstance(field.widget, RadioSelect) or isinstance(field.widget, CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'icheck'
                continue
            field.widget.attrs['class'] = 'form-control'


class StarkForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(StarkForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class Row(object):
    def __init__(self, data_list, option, query_dict, title):
        '''
        :param data_list: 元祖或queryset
        '''
        self.data_list = data_list
        self.option = option
        self.query_dict = query_dict
        self.title = title

    def __iter__(self):
        '''
        生成过滤标签
        :return:
        '''
        yield '<div class="whole">'
        yield '<a>%s</a>' % self.title
        yield '</div>'
        yield '<div class="others">'
        # 处理‘全部’标签
        total_query_dict = self.query_dict.copy()
        total_query_dict._mutable = True
        origin_value_list = self.query_dict.getlist(self.option.field)  # [2,]
        if origin_value_list:
            total_query_dict.pop(self.option.field)
            yield '<a href="?%s">全部</a>' % (total_query_dict.urlencode())
        else:
            yield '<a class="active" href="?%s">全部</a>' % (total_query_dict.urlencode())

        for item in self.data_list:  # item是元祖或者是queryset中的一个对象
            val = self.option.get_value(item)
            text = self.option.get_text(item)
            query_dict = self.query_dict.copy()
            query_dict._mutable = True

            if not self.option.is_multi:  # 处理单选情况
                # 如果val在value_list里面说明添加了这个过滤条件，如果没有则添加这个条件
                if str(val) in origin_value_list:
                    query_dict.pop(self.option.field)  # 用于实现选中后取消
                    yield '<a class="active" href="?%s">%s</a>' % (query_dict.urlencode(), text)
                else:
                    query_dict[self.option.field] = val
                    yield '<a href="?%s">%s</a>' % (query_dict.urlencode(), text)
            else:  # 多选情况
                multi_val_list = query_dict.getlist(self.option.field)
                if str(val) in origin_value_list:
                    # 已经选择了 把自己去掉
                    multi_val_list.remove(str(val))
                    query_dict.setlist(self.option.field, multi_val_list)
                    yield '<a class="active" href="?%s">%s</a>' % (query_dict.urlencode(), text)
                else:
                    multi_val_list.append(val)
                    query_dict.setlist(self.option.field, multi_val_list)
                    yield '<a href="?%s">%s</a>' % (query_dict.urlencode(), text)
        yield '</div>'


class Option(object):
    '''
    处理联合查询过滤的相关配置
    '''

    def __init__(self, field, condition=None, is_choice=False, text_func=None, value_func=None, is_multi=False,
                 is_OneToOne=False,
                 one_to_one_model=None):
        self.field = field
        self.is_choice = is_choice
        self.condition = condition
        if not condition:
            self.condition = {}
        self.text_func = text_func
        self.value_func = value_func
        self.is_multi = is_multi
        self.is_OneToOne = is_OneToOne
        self.one_to_one_model = one_to_one_model

    def get_queryset(self, _field, model_class, query_dict):
        '''
        获取需要过滤字段的ROW对象
        :param _field: list_filter字段
        :param model_class: 表
        :param query_dict: request.GET
        :return: ROW对象
        '''
        title = _field.verbose_name
        if isinstance(_field, ForeignKey) or isinstance(_field, ManyToManyField):
            row = Row(_field.related_model.objects.filter(**self.condition), self, query_dict, title)
        else:
            if self.is_choice:
                row = Row(_field.choices, self, query_dict, title)
            else:
                row = Row(model_class.objects.filter(**self.condition), self, query_dict, title)
        return row

    def get_text(self, item):
        '''
        如果text_fuc为空直接生成item字符串
        :param item:
        :return:
        '''
        if self.text_func:
            return self.text_func(item)

        return str(item)

    def get_value(self, item):
        '''
        获取每个对象的pk,用于生成联合过滤
        :param item:
        :return:
        '''
        if self.value_func:
            return self.value_func(item)

        if self.is_choice:
            return item[0]
        return item.pk


class DistinctOption(Option):
    '''
    可以额外实现对filter字段的一个去重
    '''

    def get_queryset(self, _field, model_class, query_dict):
        return Row(model_class.objects.filter(**self.condition).values_list('name').dinstinct(), self, query_dict)


class ChangeList(object):
    """
    封装列表页面需要的所有功能
    """

    def __init__(self, config, queryset, keyword, search_list, page, *args, **kwargs):
        self.keyword = keyword
        self.search_list = search_list
        self.page = page
        self.config = config
        self.action_list = [{'name': func.__name__, 'text': func.text} for func in config.get_action_list()]
        self.add_btn = config.get_add_btn()
        self.queryset = queryset
        self.list_display = config.get_list_display()
        self.list_filter = self.config.get_list_filter()
        self.args = args
        self.kwargs = kwargs

    def gen_list_filter_row(self):
        for option in self.list_filter:
            # 判断是不是一对一的情况如果是的化需要跨表
            # 如果 field = 表自己的字段    查本表的数据
            # 如果 field = ForeignKey   查关联表的字段
            if option.is_OneToOne:
                _field = option.one_to_one_model._meta.get_field(option.field)
                yield option.get_queryset(_field, option.one_to_one_model, self.config.request.GET)
            else:
                _field = self.config.model_class._meta.get_field(option.field)
                yield option.get_queryset(_field, self.config.model_class, self.config.request.GET)


class StarkConfig(object):
    '''
    生成URL和视图对应关系 + 默认配置
    '''
    list_display = ['__str__']
    model_form_class = None
    action_list = []
    search_list = []
    list_display_links = []
    order_by = ['-id']
    list_filter = []
    change_list_template = None

    def __init__(self, model_class, site, prev=None):
        self.model_class = model_class
        self.site = site
        self.request = None
        self.prev = prev
        # 保留过滤条件
        self.back_condition_key = "_filter"

    @property
    def urls(self):
        return self.get_urls(), None, None

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^(?P<pk>\d+)/change/$', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path(r'^(?P<pk>\d+)/del/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())

        return urlpatterns

    def display_checkbox(self, row=None, header=False):
        if header:
            return "选择"

        return mark_safe(r"<input type='checkbox' name='pk' value='%s'/>" % row.pk)

    def display_edit(self, row=None, header=False, *args, **kwargs):
        if header:
            return "编辑"
        return mark_safe(
            '<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a>' % self.reverse_edit_url(pk=row.pk,
                                                                                                         *args,
                                                                                                         **kwargs))

    def display_del(self, row=None, header=False, *args, **kwargs):
        if header:
            return "删除"
        return mark_safe(
            '<a href="%s"><i class="fa fa-trash-o" aria-hidden="true"></i></a>' % self.reverse_del_url(pk=row.pk, *args,
                                                                                                       **kwargs))

    def display_edit_del(self, row=None, header=False, *args, **kwargs):
        if header:
            return "操作"
        tpl = """<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a> |
           <a href="%s"><i class="fa fa-trash-o" aria-hidden="true"></i></a>
           """ % (self.reverse_edit_url(pk=row.pk, *args, **kwargs), self.reverse_del_url(pk=row.pk, *args, **kwargs),)
        return mark_safe(tpl)

    def get_url_name(self, param):
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param,)
        return '%s_%s_%s' % (app_label, model_name, param,)

    @property
    def get_list_url_name(self):
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        return self.get_url_name('add')

    @property
    def get_edit_url_name(self):
        return self.get_url_name('edit')

    @property
    def get_delete_url_name(self):
        return self.get_url_name('delete')

    def extra_urls(self):
        return []

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects

    def list_view(self, request, *args, **kwargs):

        if request.method == 'POST':
            action_name = request.POST.get('actions')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求')

            response = getattr(self, action_name)(request)
            if response:
                return response

        # 处理搜索
        search_list, keyword, con = self.search_condition(request)

        # 获取数据
        origin_queryset = self.get_queryset(request, *args, **kwargs)
        queryset = origin_queryset.filter(con).filter(**self.get_list_filter_condition(request)).order_by(
            *self.get_order_by()).distinct()
        # 全部数据
        total_set = queryset.count()

        # 携带参数
        query_params = request.GET.copy()
        query_params._mutable = True
        # 请求的URL
        base_url = self.request.path
        # ##### 处理分页 #####
        page = Pagination(total_set, request.GET.get('page'), query_params, base_url, per_page=20)
        # 获取组合搜索筛选
        list_filter = self.get_list_filter()
        try:
            # 搜索条件无法匹配到数据时可能会出现异常
            queryset = queryset[page.start:page.end]
        except Exception as e:
            print(e)
            queryset = []
        cl = ChangeList(self, queryset, keyword, search_list, page.page_html(), *args, **kwargs)

        context = {
            'cl': cl,
            'extra': self.get_extra_content(*args, **kwargs)
        }
        return render(request, self.change_list_template or 'stark/new_change_list.html', context)

    def get_extra_content(self, *args, **kwargs):
        return None

    def save(self, form, modify=False):
        return form.save()

    def get_form(self, model_form, request, modify=False, *args, **kwargs):
        form = model_form(request.POST, request.FILES)
        if modify:
            obj = kwargs.get('obj')
            form = model_form(request.POST, request.FILES, instance=obj)
        return form

    def add_view(self, request, template='stark/change.html', *args, **kwargs):
        """
         所有添加页面，都在此函数处理
         使用ModelForm实现
         :param request:
         :param template: 模板
         :return:
         """

        AddModelForm = self.get_model_form_class(True, request, None, *args, **kwargs)
        if request.method == "GET":
            form = AddModelForm()
            return render(request, template, {'form': form})

        form = self.get_form(AddModelForm, request)
        if form.is_valid():
            self.save(form)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, template, {'form': form})

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('数据不存在')
        EditModelForm = self.get_model_form_class(False, request, pk, *args, **kwargs)

        if request.method == "GET":
            form = EditModelForm(instance=obj)
            return render(request, template, {'form': form})

        form = self.get_form(EditModelForm, request, modify=True, obj=obj)
        if form.is_valid():
            self.save(form, modify=True)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, template, {'form': form})

    def delete_view(self, request, pk, *args, **kwargs):
        """
             删除页面
             :param request:
             :param pk:
             :return:
        """
        origin_list_url = self.reverse_list_url(*args, **kwargs)
        if request.method == 'GET':
            return render(request, 'stark/delete.html', {'cancel_url': origin_list_url})

        self.model_class.objects.filter(pk=pk).delete()
        return redirect(origin_list_url)

    def search_condition(self, request):
        search_list = self.get_search_list()
        keyword = request.GET.get('q', '')
        conn = Q()
        conn.connector = "OR"
        if keyword:
            for filed in search_list:
                conn.children.append(('%s__contains' % filed, keyword))
        return search_list, keyword, conn

    def reverse_list_url(self, *args, **kwargs):

        namespace = self.site.namespace
        name = '%s:%s' % (namespace, self.get_list_url_name)
        list_url = reverse(name, args=args, kwargs=kwargs)
        # 保留之前的搜索条件
        origin_condition = self.request.GET.get(self.back_condition_key)
        if not origin_condition:
            return list_url
        list_url = "%s?%s" % (list_url, origin_condition)
        return list_url

    def reverse_add_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的添加URL
        :return:
        """
        return self.reverse_commons_url(self.get_add_url_name, *args, **kwargs)

    def reverse_edit_url(self, *args, **kwargs):
        """
        生成带有原搜索条件的编辑URL
        :param args:
        :param kwargs:
        :return:
        """
        return self.reverse_commons_url(self.get_edit_url_name, *args, **kwargs)

    def reverse_del_url(self, *args, **kwargs):
        return self.reverse_commons_url(self.get_delete_url_name, *args, **kwargs)

    def reverse_commons_url(self, name, *args, **kwargs):
        name = "%s:%s" % (self.site.namespace, name,)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            add_url = base_url
        else:
            param = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = param
            add_url = "%s?%s" % (base_url, new_query_dict.urlencode())
        return add_url

    def get_list_filter_condition(self, request):
        '''
        获取组合搜索筛选
        :return:
        '''
        comb_condition = {}
        for option in self.get_list_filter():
            if option.is_multi:
                element = self.request.GET.getlist(option.field)  # tags=[1,2]
                if element:
                    comb_condition['%s__in' % option.field] = element
            else:
                value = request.GET.get(option.field)
                if not value:
                    continue
                comb_condition[option.field] = value
        return comb_condition

    def get_list_display(self):
        '''
        重新构建list_display 默认将选择，编辑和删除加进去
        :return:
        '''
        display_list = []
        display_list.extend(self.list_display)
        if not self.list_display_links:
            display_list.append(StarkConfig.display_edit)
        display_list.append(StarkConfig.display_del)
        return display_list

    def get_add_btn(self):
        return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % self.reverse_add_url())

    def get_order_by(self):
        return self.order_by

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        '''
        创建ModelForm
        :return:
        '''

        if self.model_form_class:
            return self.model_form_class

        class ModelForm(forms.ModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return ModelForm

    def get_action_list(self):
        val = []
        val.extend(self.action_list)
        return val

    def get_action_dict(self):
        val = {}
        for item in self.action_list:
            val[item.__name__] = item
        return val

    def get_search_list(self):
        val = []
        val.extend(self.search_list)
        return val

    def get_list_filter(self):
        val = []
        val.extend(self.list_filter)
        return val

    def multi_delete(self, request):
        '''
        批量删除功能
        :param request:
        :return:
        '''
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(pk__in=pk_list).delete()

        return HttpResponse('删除成功')

    multi_delete.text = '批量删除'

    def multi_init(self, request):
        pass

    multi_init.text = '批量初始化'


class AdminSite(object):
    '''
    通过admin生成url，以及对表进行注册
    '''

    def __init__(self):
        # self._registry = {}
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, stark_config=None, prev=None):
        if not stark_config:
            stark_config = StarkConfig
        # self._registry[model_class] = stark_config(model_class, site)
        self._registry.append(ModelConfigMapping(model_class, stark_config(model_class, self, prev), prev))

    def get_urls(self):
        urlpatterns = []

        for item in self._registry:
            app_label = item.model._meta.app_label
            model_name = item.model._meta.model_name
            if item.prev:
                urlpatterns.append(re_path(r'^%s/%s/%s/' % (app_label, model_name, item.prev), item.config.urls))
            else:
                urlpatterns.append(re_path(r'^%s/%s/' % (app_label, model_name), item.config.urls))
        return urlpatterns

    @property
    def urls(self):
        '''
        生成URL
        :return:
        '''
        return self.get_urls(), self.app_name, self.namespace


site = AdminSite()
