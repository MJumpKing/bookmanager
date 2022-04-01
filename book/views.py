from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from book.models import BookInfo
from django.http import JsonResponse
import json


"""
通过rest来是实现 对于数据的 增删改查

增加一本书籍
删除一本书籍
修改一本书籍
查询一本书籍
查询所有书籍


#############列表视图############
查询所有书籍
GET         books/
增加一本书籍
POST        books/

#############详情视图#############
删除一本书籍
DELETE      books/id/
修改一本书籍
PUT         books/id/
查询一本书籍
GET         books/id/

"""


# Create your views here.
class BookListView(View):
    """
    查询所有图书、增加图书
    """
    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            name=book_dict.get('name'),
            pub_date=book_dict.get('pub_date')
        )

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        }, safe=False)


class BookDetailView(View):
    """
    获取单个图书信息
    修改图书信息
    删除图书
    """
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.name = book_dict.get('name')
        book.pub_date = book_dict.get('pub_date')
        book.save()

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        book.delete()

        return JsonResponse({}, status=204)


###################################################

"""
序列化器将对象转化为字典
"""
from book.serializers import *
from book.models import *

# 1. 模拟查询一个对象
book = BookInfo.objects.get(id=1)

# 2.实例化序列化器,将对象数据传递给序列化器
# BookInfoSerializer(instance=对象, data=字典)
# 默认情况下不能传递查询结果集，如果需要的话加many=True
serializer = BookInfoSerializer(instance=book)

# 3.获取序列化器将对象转化为字典的数据
serializer.data

"""
反序列化的使用
    字典传入的数据类型要符合定义的数据类型
通过字段来验证数据
    required=True 默认True 为False字典可以不添加该字段的数据
    read_only: 只用于序列化使用 反序列化的时候忽略该字段，不传值
    write_only:只用于反序列化的使用，序列化的时候，忽略该字段，不返回值
如果数据满足类型要求，又满足选项要求，如果需要对数据进行进一步验证，实现以下方法：
    以validate_开头 接字段名字的方法
    例如：
        def validate_readcount(self, value):
            return value
"""
data = {'name':'python','pub_date':2000-1-1,'readcount':20}