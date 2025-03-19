from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user'

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    path('user/', include(router.urls)),
]