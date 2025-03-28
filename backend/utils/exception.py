from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from utils.response import FailureResponse


def custom_exception_handler(exc, context):
    msg = '请求处理失败！'
    response = exception_handler(exc, context)
    print(response.data)
    # Now add the HTTP status code to the response.
    if isinstance(exc, AuthenticationFailed):
        msg = '身份认证已过期！'
        return FailureResponse(message=msg, status=status.HTTP_401_UNAUTHORIZED)
    return FailureResponse(message=msg, status=status.HTTP_200_OK)