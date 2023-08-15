from django.core.validators import RegexValidator
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3, label="用户名")
    password = forms.CharField(min_length=3, label="密码")

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyNumForm(BootStrapModelForm):
    mobile_regex = r'^\+?1?\d{9,15}$'  # 定义手机号码的正则表达式
    mobile_validator = RegexValidator(
        regex=mobile_regex,
        message="手机号格式错误"
    )

    mobile = forms.CharField(validators=[mobile_validator], max_length=50)

    class Meta:
        model = models.PrettyNum
        fields = '__all__'
        # fields = ['mobile', 'price', 'level', 'status']
        # exclude = ['level']  表示排除某个字段

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


class PrettyNumEditForm(BootStrapModelForm):
    mobile_regex = r'^\+?1?\d{9,15}$'  # 定义手机号码的正则表达式
    mobile_validator = RegexValidator(
        regex=mobile_regex,
        message="手机号格式错误"
    )

    mobile = forms.CharField(validators=[mobile_validator], max_length=50, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = '__all__'
        # fields = ['mobile', 'price', 'level', 'status']
        # exclude = ['level']  表示排除某个字段

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        instance_id = self.instance.id  # 获取当前行的 ID
        exists = models.PrettyNum.objects.exclude(id=self.instance.id).filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


