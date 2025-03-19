from rest_framework.pagination import PageNumberPagination

from utils.response import SuccessResponse


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 500
    page_query_param = 'page'
