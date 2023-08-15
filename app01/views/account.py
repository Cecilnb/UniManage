from django.shortcuts import render, HttpResponse, redirect
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}, render_value=True))
    code = forms.CharField(label="验证码",
                           widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # {'username': 'erog', 'password': 'boigi'}
        # print(form.cleaned_data)
        # {'username': 'erog', 'password': 'b9eac0d4fc8c0220b6cb4dbb02284892'}

        # 验证码的校验，从form.cleaned_data中剔除式校验
        user_input_code = form.cleaned_data.pop('code')  # 而不是用get
        code = request.session.get('image_code', '')  # 可能为空 ，因为设置了60s超时
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")  # 把错误信息展示到密码框下面了
            return render(request, 'login.html', {"form": form})   # 后面代码就不会执行了

        # 去数据库校验用户名和密码是否正确,获取用户对象
        # admin_object = models.Admin.objects.filter(username="xxx", password="xxx").first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")  # 把错误信息展示到密码框下面了
            return render(request, 'login.html', {"form": form})  # 会直接返回验证码错误；

        # 用户名和密码正确,登录成功后
        # 网站生成随机字符串;写到用户浏览器的cookie中;再写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # 登录成功并且设置了在session中设置了用户信息之后，session可以保存七天
        request.session.set_expiry(60*60*24*7)

        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})


def logout(request):
    """注销"""

    request.session.clear()

    return redirect("/login/")


from app01.utils.code import check_code
from io import BytesIO


def image_code(request):
    """生成图片验证码"""

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码在进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    image_stream = BytesIO()
    img.save(image_stream, format='PNG')

    return HttpResponse(image_stream.getvalue())
