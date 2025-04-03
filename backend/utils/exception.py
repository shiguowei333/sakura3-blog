from django.db.models import ProtectedError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from utils.response import FailureResponse


def custom_exception_handler(exc, context):

    msg = '请求处理失败！'
    print(exc)
    # Now add the HTTP status code to the response.
    if isinstance(exc, AuthenticationFailed):
        msg = '身份认证已过期！'
        return FailureResponse(message=msg, status=status.HTTP_401_UNAUTHORIZED)
    elif isinstance(exc, Http404):
        msg = '接口地址错误！'
        return FailureResponse(message=msg, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, ProtectedError):
        msg = '该数据被其他数据关联，无法删除！'
        return FailureResponse(message=msg, status=status.HTTP_200_OK)
    elif isinstance(exc, APIException):
        msg = '请求处理失败！'
        return FailureResponse(message=msg, status=status.HTTP_200_OK)
    else:
        msg = '服务器异常！'
        return FailureResponse(message=msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)