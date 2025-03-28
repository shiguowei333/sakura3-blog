"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from apps.user import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API文档",
        default_version="v1",
        description="sakura_admin系统接口文档",
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
# Swagger UI
    path('api/admin/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('api/admin/auth/login', permissions.LoginView.as_view(), name='login'),
    path('api/admin/auth/token/refresh', permissions.RefreshView.as_view(), name='refresh'),
    path('api/admin/info/', include('apps.user.urls')),
    path('api/admin/tag/', include('apps.tag.urls')),
    path('api/admin/category/', include('apps.category.urls'))
]
