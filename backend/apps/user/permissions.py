from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from utils.response import SuccessResponse, FailureResponse, DetailResponse
from .serializers import LoginReqSerializer, UserSerializer


# Create your views here.
# 登录视图
class LoginView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginReqSerializer(data=request.data)
        # 登录参数序列化器校验
        if not serializer.is_valid():
            return FailureResponse(message=serializer.errors)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        # 登录校验
        user = authenticate(username=username, password=password)
        if user is None:
            return FailureResponse(message='用户名或密码错误',status=status.HTTP_200_OK)
        # 获取token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # 计算过期时间
        current_time = timezone.now()
        expiration_time = current_time + access_token.lifetime
        expiration_time_str = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data = UserSerializer(user).data
        data = {
            'avatar': user_data['avatar'],
            'username': user_data['username'],
            'nickname': user_data['nick_name'],
            'accessToken': str(access_token),
            'refreshToken': str(refresh),
            'expires': expiration_time_str
        }
        return DetailResponse(data=data, message='登录成功！')

# 刷新令牌视图
class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        current_time = timezone.now()
        refresh_token = request.data.get('refresh')
        # 调用父类的 post 方法来获取默认的响应
        try:
            # 获取原始数据
            response = super().post(request, *args, **kwargs)
            original_data = response.data
            access_token = original_data.get('access')
            # 计算访问令牌的到期时间
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            expiration_time = current_time + access_token_lifetime
            expiration_time_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'accessToken': access_token,
                'refreshToken': refresh_token,
                'expires': expiration_time_str
            }
            return DetailResponse(data=data, message="令牌刷新成功！")
        except:
            # 处理错误响应
            return FailureResponse(message="令牌已失效！", status=status.HTTP_401_UNAUTHORIZED)

