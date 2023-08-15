"""
自定义的分页组件,以后如果想要使用这个分页组件，你需要做如下几件事

在视图函数中：
    def prettynum_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        page_queryset = page_object.page_queryset
        page_string = page_object.html()

        context = {
            "queryset": page_queryset,  # 分完页的数据
            # "search_data": search_data,
            "page_string": page_string  # 页码
        }

        return render(request, 'prettynum_list.html', context)

在html中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/prettynum/list/?page=12
        :param plus: 显示当前页的前几页 或后几页
        """

        self.get_params = request.GET.copy()  # 复制QueryDict对象，产生一个可修改的副本
        # # 修改副本中的参数值
        # self.get_params['param'] = 'new_value'
        # # 获取修改后的URL编码字符串
        # encoded_params = self.get_params.urlencode()

        self.page_param = page_param  # 页面参数
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()  # 符合条件的总数据
        # 得到总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:  # 余数不是零，就还要加1
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出当前页 的前五页 和 后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少时，都没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:  # 总页码>11
            # 当前页<5时，（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页>5
                # 当前页+5 > 总页码
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:  # 当前页+5 < 总页码
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        # 首页
        # 添加副本中的参数值
        self.get_params.setlist(self.page_param, [1])
        # 获取修改后的URL编码字符串
        encoded_params = self.get_params.urlencode()
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(encoded_params))

        # 上一页
        if self.page > 1:
            self.get_params.setlist(self.page_param, [self.page - 1])
            encoded_params = self.get_params.urlencode()
            prev = '<li><a href="?{}">«</a></li>'.format(encoded_params)
        else:
            self.get_params.setlist(self.page_param, [1])
            encoded_params = self.get_params.urlencode()
            prev = '<li><a href="?{}">«</a></li>'.format(encoded_params)
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.get_params.setlist(self.page_param, [i])
            encoded_params = self.get_params.urlencode()
            # 格式化字符串
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(encoded_params, i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(encoded_params, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.get_params.setlist(self.page_param, [self.page + 1])
            encoded_params = self.get_params.urlencode()
            prev = '<li><a href="?{}">»</a></li>'.format(encoded_params)
        else:
            self.get_params.setlist(self.page_param, [self.total_page_count])
            encoded_params = self.get_params.urlencode()
            prev = '<li><a href="?{}">»</a></li>'.format(encoded_params)
        page_str_list.append(prev)

        # 尾页
        self.get_params.setlist(self.page_param, [self.total_page_count])
        encoded_params = self.get_params.urlencode()
        page_str_list.append('<li><a href="?">尾页</a></li>'.format(self.total_page_count))

        search_string = """
        <li>
        <form style="float: left;margin-left: -1px" method="get">
        <input name="page"
        style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
        type="text" class="form-control" placeholder="页码">
        <button class="btn btn-default" type="submit">跳转</button>
        </form>
        </li>
        """

        page_str_list.append(search_string)

        # 将列表转化为字符串
        page_string = mark_safe("".join(page_str_list))
        return page_string
