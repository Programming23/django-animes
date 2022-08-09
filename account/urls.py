from os import terminal_size
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import *

urlpatterns = [
    #path('register/', views.register, name='register'),
    path('', views.account, name='account'),
    #path('login/', views.login, name='login'),
    #path('reset-password/', views.reset_password, name='reset_password'),
    #path('reset-password/<uidb64>/<token>/', views.reset_password_confirm, name="password_reset_confirm"),
    #path('user/<str:username>/', views.user_profile, name='user_profile'),
    #path('user/<str:username>/<str:inf>/', views.account_animes, name='account_animes'),
    #path('logout/', views.logout, name='logout'),
    path('list/<str:slug>/', views.list, name='list'),
    path('animes-favorite/<str:name>/', views.animes_favorites_check, name='animes_favorite_check'),
    #path('animes-favorite/', views.animes_favorites, name='animes-favorite'),
    path('list/completed/<str:name>/', views.done_show_check, name='done_show_add'),
    path('list/plan-to-watch/<str:name>/', views.want_show_check, name='want_show_add'),
    path('list/watching/<str:name>/', views.watching_check, name='watching_add'),
    path('list/watch-later/<str:name>/', views.later_check, name='later_add'),
    path('list/dropped/<str:name>/', views.dropped_check, name='dropped_add'),
    #path('activate-user/<uidb64>/<token>/', views.activate, name='activate'),
    path('delete-from-list/<str:name>/', views.delete_from_list, name='delete_from_list'),
]