# 对drf的响应进行二次封装

from rest_framework.response import Response
from rest_framework import status

"""
    基础通用响应，封装符合restful规范的json数据格式
    code: 业务状态码
    success: 执行成功/失败
    message: 提示信息
    data: 执行成功返回数据
"""
class BaseResponse(Response):
    def __init__(self, code, success, message, data=None, status=status.HTTP_200_OK, template_name=None, headers=None, exception=False, content_type=None):
        response_json = {
            "code": code,
            "success": success,
            "message": message
        }
        if data is not None:
            response_json["data"] = data
        super().__init__(response_json, status, template_name, headers, exception, content_type)


# 数据查询标准响应成功的返回，业务码默认为2000
class SuccessResponse(BaseResponse):
    def __init__(self, data=None, message='请求处理成功！', page=1, limit=1, total=1):
        if not data:
            total = 0
        data_json = {
            "page": page,
            "limit": limit,
            "total": total,
            "records": data
        }
        super().__init__(2000, True, message, data_json, status.HTTP_200_OK)

# 不包含分页的数据标准成功响应
class DetailResponse(BaseResponse):
    def __init__(self, data=None, message='请求处理成功！', headers=None):
        super().__init__(2000, True, message, data, status.HTTP_200_OK, headers=headers)

# 标准响应失败的返回，业务码默认返回0，自定义返回data数据和message
class FailureResponse(BaseResponse):
    def __init__(self, message='请求处理失败！', status=status.HTTP_400_BAD_REQUEST):
        super().__init__(0, False, message, status=status)
