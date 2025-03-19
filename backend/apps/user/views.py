from pyexpat.errors import messages
from rest_framework import viewsets
from rest_framework.decorators import action

from utils.response import DetailResponse
from utils.viewset import CustomViewSet
from .models import User
from .serializers import UserSerializer


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', '')
        telephone = self.request.query_params.get('telephone', '')
        is_active = self.request.query_params.get('is_active', '')
        self.queryset =  self.queryset.filter(username__icontains=username, telephone__icontains=telephone)
        if is_active != '':
            return self.queryset.filter(is_active=is_active)
        return self.queryset
