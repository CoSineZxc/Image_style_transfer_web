from django.urls import path
from django.conf.urls import url
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_picture', views.upload_picture, name='upload_picture'),
    path('trans_picture', views.trans_picture, name='trans_picture'),
]
