from rest_framework import status
from rest_framework.views import APIView

from utils.response import FailureResponse, DetailResponse
from .serializers import UserSerializer


class UserInfo(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return DetailResponse(message="修改成功")
        else:
            return FailureResponse(message=serializer.errors)

