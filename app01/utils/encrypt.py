from django.conf import settings
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 用salt作为参数直接创建md5对象
    obj.update(data_string.encode('utf-8'))  # 通过update方法逐步把参数传递给md5对象
    return obj.hexdigest()
