import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import WebInfo


User = get_user_model()


# 登录请求序列化器，可以在此处添加登录表单的校验
class LoginReqSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class JsonListField(serializers.Field):
    # 序列化时：将数据库中的字符串转为JSON列表返回给前端
    def to_representation(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return value

    # 反序列化时：将前端传入的JSON列表转为字符串存储到数据库
    def to_internal_value(self, data):
        if isinstance(data, list):
            return json.dumps(data)
        raise serializers.ValidationError("必须为有效的JSON列表格式")


# 站长信息的列化器，更新站长信息
class UserSerializer(serializers.ModelSerializer):
    bg_img = JsonListField()
    class Meta:
        model = User
        fields = ['nick_name', 'avatar', 'title', 'bg_img', 'github_url']


# 网站信息的序列化器，更新网站信息
class WebSerializer(serializers.ModelSerializer):
    web_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    slideshow = JsonListField()
    class Meta:
        model =WebInfo
        fields = ['web_name', 'header_inform', 'aside_inform', 'archival_inform', 'slideshow', 'web_time']