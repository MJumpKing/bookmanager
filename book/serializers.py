
"""
drf 框架 帮助实现 序列化和反序列化的功能（对象和字典的相互转换）

BookInfo(对象)        ------序列化器类------>           字典

序列化器类
    1.将对象转换为字典

class 序列化器名字(serializers.Serializer)
    子段名 = serializer.类型(选项)

    字段名和模型字段名一致
    字段的类型和模型的类型一致
"""
from rest_framework import serializers


# 关系型数据库外键查询
class PeopleRelatedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.DateField()


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField()
    pub_date = serializers.DateField(required=True)
    readcount = serializers.IntegerField(required=False)
    commentcount = serializers.IntegerField(required=False)
    # 查询所有人物的信息，再创建个序列化器
    people = PeopleRelatedSerializer(many=True, required=False)
    # 反序列化对readcount字段传入的值检测

    # 检测单一数据
    def validate_readcount(self, value):
        if value < 0:
            # raise Exception('阅读量不能为复数')
            raise serializers.ValidationError('阅读量不能为复数')
        return value

    # 多个字段检测
    # attrs=data
    def validate(self, attrs):
        readcount = attrs.get('readcount')
        commentcount = attrs.get('commentcount')
        if readcount <= commentcount:
            raise serializers.ValidationError('评论量大于阅读量')
        return attrs


class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.DateField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    # 外键
    # 1.如果定义的序列化器外外键类型为IntegerField，那么对应的序列化字段名必须和数据库中的外键字段名一致
    # book_id = serializers.IntegerField()

    # 2.如果期望的数据外键数据的key就是模型字段的名字， 那么PrimaryKeyRelatedField就可以获取到关联的模型id值
    # queryset 在验证数据的时候，要告诉系统在那里匹配外键数据
    # book = serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())
    # 或者
    # read_only=True 只读，不验证数据
    # book = serializers.PrimaryKeyRelatedField(read_only=True)

    # 3. 如果期望获取外键关联的字符串信息， 使用StringRelatedField
    # 返回关系模型中 __str__ 的数据
    # book = serializers.StringRelatedField()

    # 4.期望获取关联模型中所有数据，这个时候定义book = BookInfoSerializer()
    # book=关联的BookInfo的一个关联对象数据
    # book=BookInfo.objects.get(id=xxxx)
    # book = BookInfoSerializer(book).data
    book = BookInfoSerializer()


