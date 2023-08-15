from django.shortcuts import render, redirect
from app01.utils.pagination import Pagination
from app01 import models
from app01.utils.forms import UserModelForm, PrettyNumForm, PrettyNumEditForm


# Create your views here.
def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户 """
    if request.method == "GET":
        queryset = models.Department.objects.all()
        return render(request, "user_add.html", {"queryset": queryset})

    # 获取用户提交的数据

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")


# ##################################### modelForm 示例 ###############################


def user_model_form_add(request):
    """添加用户（ModelForm版本)"""
    if request.method == "GET":
        form = UserModelForm()  # 实例化对象
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)  # 将请求体中数据以参数的形式传递给  ，
    if form.is_valid():  # 校验成功
        # 如果数据合法，保存到数据库
        # models.UserInfo.objects.create(……)
        # 因为ModelForm 知道获取数据后，可能会提交
        form.save()  # 自动存储到models中关联类的数据表中  因为继承ModelForm定义类时，要写model = models.UserInfo    指定了model（数据表）
        # print(form.cleaned_data)
        return redirect('/user/list')

    else:  # 校验失败
        # 在页面上显示错误信息，那个字段出错了，就显示那个字段的错误信息
        # print(form.errors)  #form.errors   form封装了每一个字段的错误信息
        return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    if request.method == "GET":
        row_object = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()  # 会保存数据到数据库，但是默认是以添加的方式保存，如果要以更新的方式保存那就得，在实例化form对象时，指定instance参数的值对象
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
