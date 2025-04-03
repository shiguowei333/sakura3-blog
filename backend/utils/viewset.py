from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet

from .pagination import CustomPagination
from .response import DetailResponse, SuccessResponse, FailureResponse


class CustomViewSet(ModelViewSet):
    """
    自定义ModelViewSet,使用统一的响应格式
    """

    pagination_class = CustomPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return DetailResponse(message="新增成功！", headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DetailResponse(serializer.data, message="查询成功！")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return DetailResponse(message="修改成功！")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return DetailResponse(message="删除成功！")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return SuccessResponse(serializer.data, message="查询成功！", page= request.query_params.get('page'), limit= request.query_params.get('limit'), total=queryset.count())

        serializer = self.get_serializer(queryset, many=True)
        return DetailResponse(serializer.data, message="查询成功！")
