from django.urls import path

from utils.upload import SlideUploadView
from . import views

app_name = 'user'


urlpatterns = [
    path('user', views.UserInfoView.as_view()),
    path('web', views.WebInfoView.as_view()),
    path('web/upload', SlideUploadView.as_view(), name='upload'),
]