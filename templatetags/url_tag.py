# -*- coding: utf-8 -*-
import time
from django.conf import settings
from django import template

register = template.Library()


def build_url(path):
    return path


def build_static_url(path):
    release_version = app.config.get('RELEASE_VERSION')
    ver = "%s" % (int(time.time())) if not release_version else release_version
    path = "/static" + path + "?ver=" + ver
    return buildUrl(path)


def build_image_url(path):
    app_config = app.config['APP']
    url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
    return url
