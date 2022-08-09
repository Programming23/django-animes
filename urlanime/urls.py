from django.urls import path, re_path
from . import views

urlpatterns = [
    path('أنمي_<str:name>_<str:typ>_<str:episode>/', views.watch, name='watch'),
    path('<str:slug>/', views.anime, name='anime'),
    
    
]