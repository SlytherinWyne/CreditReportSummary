# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse
import xlrd

import model.Focus as f
import model.Summary as s

# Create your views here.


def index(request):
    return HttpResponse("Hello World!")


def upload(request):
    return render(request, 'xxx.html')


def summary(request):
    excel = request.FILES.getlist('excel')[0]
    data = xlrd.open_workbook(file_contents=excel.read())
    focus_list = f.get_focus(data)
    dict = {}
    for i in range(len(focus_list)):
        summary_list = []
        for line in focus_list[i]:
            line = line.encode('utf-8')
            summary = s.get_summary(line)
            summary.insert(0, line)
            summary_list.append(summary)
        dict[str(i + 1)] = summary_list
    return HttpResponse(HttpResponse(json.dumps(dict), content_type="application/json"))
