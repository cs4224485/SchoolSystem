# -*- coding: utf-8 -*-
import time
from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag
def build_url(path):
    return path


@register.simple_tag
def build_static_url(path):
    release_version = settings.RELEASE_VERSION
    ver = "%s" % (int(time.time())) if not release_version else release_version
    path = "/static" + path + "?ver=" + ver
    return build_url(path)


# def build_image_url(path):
#     app_config = app.config['APP']
#     url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
#     return url
