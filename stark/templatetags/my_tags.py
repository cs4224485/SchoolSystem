# Author: harry.cai
# DATE: 2018/9/16
from django import template
from django.db.models import ManyToManyField
from django.utils.safestring import mark_safe
register = template.Library()


def header_list(cl):
    """
    表头
    :param cl:
    :return:
    """

    for head in cl.config.get_list_display():
        if callable(head):
            val = head(cl, header=True)
        else:
            if head == '__str__':
                val = cl.config.model_class._meta.model_name.upper()
            else:
                val = cl.config.model_class._meta.get_field(head).verbose_name
        yield val


def body_list(cl):
    """
    表格内容
    :param cl:
    :return:
    """
    body_list = []
    for query_obj in cl.queryset:
        row = []
        for field in cl.list_display:
            if callable(field):
                # 如果display中的字段是一个函数
                value = field(cl.config, row=query_obj)
            else:
                  try:  # 如果filed __str__ 需要捕捉异常处理
                    field_obj = cl.config.model_class._meta.get_field(field)

                    # 多对多字段展示方法
                    if isinstance(field_obj, ManyToManyField):
                        ret = getattr(query_obj, field).all()
                        t = []
                        for mobj in ret:
                            t.append(str(mobj))
                        value = ",".join(t)
                    else:
                        # 捕获choices字段
                        if field_obj.choices:
                            value = getattr(query_obj, "get_" + field + "_display")
                        else:
                            value = getattr(query_obj, field)
                        # 如果字段是一个link类型字段那么给它构建一个a标签
                        if field in cl.config.list_display_links:
                            _url = cl.config.reverse_edit_url(query_obj)
                            value = mark_safe("<a href='%s'>%s</a>" % (_url, value))
                  except Exception:
                      value = getattr(query_obj, field)
            row.append(value)
        body_list.append(row)
    return body_list


@register.inclusion_tag('stark/table_body.html')
def table(cl):
    return {'header_list': header_list(cl), 'body_list': body_list(cl)}