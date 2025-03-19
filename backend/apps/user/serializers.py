from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


# 登录请求序列化器，可以在此处添加登录表单的校验
class LoginReqSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

# 站长信息的列化器，返回user表中需要的数据
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nick_name', 'avatar', 'title', 'bg_img', 'github_url']


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance