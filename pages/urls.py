from django.urls import path, re_path
from pages import views, accounts, api
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', views.index, name='index'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('admin/login/', views.page_reset, name='admin-login'),
    path('قائمة-الأنمي/', views.list_anime, name='list_anime'),
    path('episode/', views.episode, name='episode'),
    path('login/', accounts.login, name='login'),
    path('register/', accounts.register, name='register'),
    path('logout/', accounts.logout, name='logout'),
    path('animelek/<user>/<passw>/episodes/', api.animelek_episodes, name='animelek_episodes'),
    path('check_user/<user>/<passw>/', api.check_user, name='check_user'),
    #path('<user>/<passw>/export/', api.export, name='export'),
    path('animelek/<user>/<passw>/animes/', api.get_animes, name='get_animes_api'),
    path('animelek/<user>/<passw>/insert_animes/', api.animelek_insert_animes, name='animelek_insert_animes_api'),
    path('animelek/<user>/<passw>/insert_episodes/', api.animelek_insert_episodes, name='animelek_insert_episodes_api'),
    path('reset-password/', accounts.reset_password, name='reset_password'),
    path('reset-password/<uidb64>/<token>/', accounts.reset_password_confirm, name="password_reset_confirm"),
    path('activate-user/<uidb64>/<token>/', accounts.activate, name='activate'),
    path('مواعيد-عرض-حلقات-الانمي/', views.days_anime, name='days_anime')
]