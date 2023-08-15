from django.shortcuts import render, redirect
from app01.utils.pagination import Pagination
from app01 import models
from app01.utils.forms import UserModelForm, PrettyNumForm, PrettyNumEditForm


# Create your views here.


def prettynum_list(request):
    """ 靓号列表 """

    get_object = request.GET.copy()  # 复制QueryDict对象，产生一个可修改的副本
    # 修改副本中的参数值
    # get_object.setlist('page', [11])
    # 获取修改后的URL编码字符串
    # encoded_object = get_object.urlencode()
    # print(encoded_object)

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "queryset": page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_string  # 页码
    }

    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    if request.method == "GET":
        form = PrettyNumForm()
        return render(request, 'prettynum_add.html', {"form": form})

    form = PrettyNumForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    return render(request, 'prettynum_add.html', {"form": form})


def prettynum_edit(request, nid):
    if request.method == "GET":
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyNumEditForm(instance=row_object)
        return render(request, "prettynum_edit.html", {"form": form})

    else:
        row_object = models.PrettyNum.objects.filter(id=nid).first()
        form = PrettyNumEditForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect("/prettynum/list/")
        else:
            return render(request, "prettynum_edit.html", {"form": form})


def prettynum_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/prettynum/list/")
