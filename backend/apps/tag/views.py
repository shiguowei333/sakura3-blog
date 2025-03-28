from django.shortcuts import render
from rest_framework import viewsets

from utils.pagination import CustomPagination
from utils.viewset import CustomViewSet
from .models import Tag
from .serializers import TagSerializer


# Create your views here.

class TagViewSet(CustomViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name:
            return self.queryset.filter(tag_name__icontains=name)
        else:
            return self.queryset