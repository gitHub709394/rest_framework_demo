from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from rest_framework import serializers
from rest_framework.response import Response
from .models import *
import json


# Create your views here.

class ParserDemo(APIView):
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        return HttpResponse("ok")

    def post(self, request, *args, **kwargs):
        print(request.data)
        return HttpResponse("ok")

    def put(self, request, *args, **kwargs):
        print(request.data)
        return HttpResponse("ok")

    def delete(self, request, *args, **kwargs):
        print(request.data)
        return HttpResponse("ok")


class RoleSerialzers(serializers.Serializer):
    id = serializers.IntegerField()
    role_name = serializers.CharField()


class SerializersDemo(APIView):
    def get(self, request, *args, **kwargs):
        ser = RoleSerialzers(instance=Role.objects.all(), many=True)
        return HttpResponse(json.dumps(ser.data, ensure_ascii=False), content_type="application/json")


class UserValidate(object):

    def __init__(self, input):
        self.input = input

    def __call__(self, value, *args, **kwargs):
        if value != self.input:
            message = f"用户名必须为{self.value}"
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        pass


class UserInfoSerializers(serializers.Serializer):
    # user_name = serializers.CharField(error_messages={"required": "用户名不能为空"}, validators=[UserValidate("你好")])
    user_name = serializers.CharField(error_messages={"required": "用户名是必须的", "blank": "用户名不能为空"})
    user_type_name = serializers.CharField(source="get_user_type_display")
    user_type_id = serializers.CharField(source="user_type")
    group = serializers.CharField(source="group.group_name")
    roles = serializers.SerializerMethodField()

    def get_roles(self, row):
        # row 就是指向每一行的userInfo对象
        roles = []
        for item in row.roles.all():
            roles.append({
                "role_name": item.role_name,
                "id": item.id
            })
        return roles

    # 验证钩子函数
    # def validate_字段(self, validated_value):
    #     raise ValidationError(detail='xxxxxx')
    #     return validated_value
    def validate_user_name(self, validate_value):
        if validate_value.strip() != "123":
            raise serializers.ValidationError(detail='用户名只能是123')
        return validate_value


class SerializersUserInfo(APIView):
    def get(self, request, *args, **kwargs):
        ser = UserInfoSerializers(instance=UserInfo.objects.all(), many=True)
        return HttpResponse(json.dumps(ser.data, ensure_ascii=False), content_type="application/json")

    def post(self, request, *args, **kwargs):
        # 对数据验证
        ser = UserInfoSerializers(data=request.data)
        if ser.is_valid():
            return HttpResponse("ok")
        else:
            print(ser.validated_data)
            return Response(ser.errors)


from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = "page_size"

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 2


from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView


class PageRoles(APIView):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()

        # 先分页
        page = CursorPagination()
        page_list = page.paginate_queryset(queryset=roles, request=request, view=self)

        # 再序列化
        roles_ser = RoleSerialzers(instance=page_list, many=True)

        return page.get_paginated_response(data=roles_ser.data)
