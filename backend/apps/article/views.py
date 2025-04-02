from django.shortcuts import render

from utils.pagination import CustomPagination
from utils.response import SuccessResponse, DetailResponse
from .models import Article
from .serializers import ArticleSerializer, HandlerArticleSerializer
from utils.viewset import CustomViewSet


# Create your views here.

class ArticleViewSet(CustomViewSet):
    queryset = Article.objects.all()
    serializer_class = HandlerArticleSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ArticleSerializer(page, many=True)
            return SuccessResponse(serializer.data, message="查询成功！", page= request.query_params.get('page'), limit= request.query_params.get('limit'), total=queryset.count())

        serializer = ArticleSerializer(queryset, many=True)
        return DetailResponse(serializer.data, message="查询成功！")

    def get_queryset(self):
        title = self.request.query_params.get('title')
        category = self.request.query_params.get('category')
        if title:
            self.queryset = self.queryset.filter(title__icontains=title)
        if category:
            self.queryset = self.queryset.filter(article_category=category)
        return self.queryset
