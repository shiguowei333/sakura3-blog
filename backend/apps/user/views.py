from rest_framework.views import APIView

from utils.response import FailureResponse, DetailResponse
from .serializers import UserSerializer, WebSerializer


class UserInfoView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return DetailResponse(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return DetailResponse(message="修改成功")
        else:
            return FailureResponse(message=serializer.errors)

class WebInfoView(APIView):
    def get(self, request):
        serializer = WebSerializer(request.user.web_info)
        return DetailResponse(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = WebSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user.web_info, serializer.validated_data)
            return DetailResponse(message="修改成功")
        else:
            return FailureResponse(message=serializer.errors)
