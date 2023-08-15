import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination

datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    form = OrderModelForm()

    context = {
        "form": form,  # 用于生成模态框的输入元素
        # 用于实现表格和分页
        "queryset": page_queryset,  # 分完页的数据
        # "search_data": search_data,
        "page_string": page_string  # 生成页码
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单（Ajax请求）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号: 额外增加一些不是用户输入的值(自己计算出来)
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]

        # 保存到数据库
        form.save()
        return JsonResponse({"status": True})
        # return HttpResponse(json.dumps({"status": True}))

    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    models.Order.objects.filter(id=uid).delete()
   