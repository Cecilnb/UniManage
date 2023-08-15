import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    # 重定义表单字段
    detail = forms.CharField(max_length=100, widget=forms.TextInput())

    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            # "detail": forms.Textarea
            "detail": forms.TextInput
        }


def task_list(request):
    """任务列表"""
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, "task_list.html", context)


def task_ajax(request):
    print(request.GET)
    print(request.POST)

    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


def task_add(request):
    # <QueryDict: {'csrfmiddlewaretoken': ['TvCog0fpW8Tue2MLzPcrYMjwVtOI0CYuSTfVjLfgesO0yrA4xioqEWWWPYLye57H'], 'level': ['2'], 'title': ['企业部'], 'detail': ['aegh'], 'user': ['8']}>
    print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm）校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    # 校验失败
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))