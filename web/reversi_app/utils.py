#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Shiyu Huang
# @File    : utils.py

from flask import render_template


def myRender(name_now, uurl, **context):
    # prefix = name_now.split('.')
    # prestring = prefix[0] + '/' + '.'.join(prefix[1:])
    print(name_now + '/index.html')

    return render_template(name_now + '/' + uurl, **context)
