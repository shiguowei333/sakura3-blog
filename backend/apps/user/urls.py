from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('user/', views.UserInfo.as_view()),
]