from django.db import models


# Create your models here.

class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="姓名", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    gender_choices = (
        (1, "男"),
        (2, "女")
    )

    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    mobile = models.CharField(max_length=50, verbose_name='手机号')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')

    LEVEL_CHOICES = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='级别')

    STATUS_CHOICES = (
        (1, '未占用'),
        (2, '已占用'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name='状态')


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """订单"""
    STATUS_CHOICES = (
        (1, "已支付"),
        (2, "待支付"),
    )

    oid = models.CharField(verbose_name="订单号", max_length=50)
    title = models.CharField(verbose_name="商品名称", max_length=100)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    status = models.SmallIntegerField(verbose_name="状态", choices=STATUS_CHOICES, default=2)
    admin = models.ForeignKey(Admin, verbose_name="管理员", on_delete=models.CASCADE)

    def __str__(self):
        return self.oid

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

