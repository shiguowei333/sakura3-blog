from django.shortcuts import render
from rest_framework import viewsets

from utils.viewset import CustomViewSet
from .models import Tag
from .serializers import TagSerializer


# Create your views here.

class TagViewSet(CustomViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer