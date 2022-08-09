
from django.conf.urls import url
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.admin.models import *
from django.contrib import auth
from pages.models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import  force_bytes, force_str, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
import re
from django.conf import settings
from .utils import generate_token
from django.urls import path, include
from django.http import *
import secrets
import time
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from pages.views import get_client_ip
# Create your views here.
import requests


    #return render(request, 'pages/index.html')

def user_profile(request, username):
    domain = get_current_site(request)

    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    try:
        user_back = UsersBack.objects.get(user=user, information_public=True)
    except:
        raise Http404
    x = {
        'user': user_back,
        'domain': domain,
        'title_tag': username
    }

    return render(request, 'users/user-profile.html', x)

def account_animes(request, username, inf):
    domain = get_current_site(request)
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    try:
        user_back = UsersBack.objects.get(user=user, information_public=True)
    except:
        raise Http404

    if inf == 'الأنميات-المفضلة' :
        paginator = Paginator(user_back.animes_fav.all(), 24)
        title = 'الأنميات المفضلة'

    elif inf == 'تم-مشاهدتها':
        paginator = Paginator(user_back.animes_done.all(), 24)
        title = 'أنميات تم مشاهدتها'

    elif inf == 'أرغب-بمشاهدتها':
        paginator = Paginator(user_back.animes_want.all(), 24)
        title = 'أنميات أرغب بمشاهدتها'

    else:
        raise Http404

    s = 1
    title = 'الأنميات المفضلة'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()

    if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']



    try:
        page = paginator.page(s)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    if page.number <= 1:
        page.range = range(page.number, paginator.num_pages+1)[:3]
    elif page.number == 2:
        page.range = range(page.number-1, paginator.num_pages+1)[:4]
    else:
        page.range = range(page.number-2, paginator.num_pages+1)[:5]



    for anime in page:
        anime.url_anime = urlsafe_base64_encode(force_bytes(anime.name))
        anime.title = anime.name.title()

    for i in anime_class:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_state:
        i.url_anime = i.name.replace(' ', '-')

    for i in anime_type:
        i.url_anime = i.name.replace(' ', '-')

    x = {
        'title': title,
        'page': page,
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'domain': domain,
        'title_tag': username
    }
    if request.user.is_authenticated:
        x['user'] = request.user.user

    return render(request, 'pages/list-anime.html', x)




def account(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user = UsersBack.objects.get(user=request.user, is_active=True)
    except:return redirect('login')
    user.now_show = user.animes_now.count
    user.fav = user.animes_fav.count
    user.last = user.last_animes.count
    user.want_show = user.animes_want.count
    user.later_show = user.animes_later.count
    user.done_show = user.animes_done.count
    user.dont_show = user.animes_dont.count

    context = {
        'user': user,
        'domain': get_current_site(request)
    }
    return render(request, 'account/profile.html', context)


# animes user



def animes_favorites_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            user_back = UsersBack.objects.get(user=request.user)
            if UsersBack.objects.filter(user=request.user, animes_fav=anime).exists():
                user_back.animes_fav.remove(anime)
                res = False
            else:
                user_back.animes_fav.add(anime)
                res = True

            return JsonResponse({'res': res})
        raise Http404
    else:
        return redirect('login')





def done_show_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            done = UsersBack.objects.get(user=request.user)


            if not( UsersBack.objects.filter(user=request.user, animes_done=anime).exists()):
                done.animes_done.add(anime)
                done.animes_want.remove(anime)
                done.animes_now.remove(anime)
                done.animes_later.remove(anime)
                done.animes_dont.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')



def want_show_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            want = UsersBack.objects.get(user=request.user)

            if not(UsersBack.objects.filter(user=request.user, animes_want=anime).exists()):
                want.animes_want.add(anime)
                want.animes_done.remove(anime)
                want.animes_now.remove(anime)
                want.animes_later.remove(anime)
                want.animes_dont.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')

def watching_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            want = UsersBack.objects.get(user=request.user)

            if not(UsersBack.objects.filter(user=request.user, animes_now=anime).exists()):
                want.animes_now.add(anime)
                want.animes_done.remove(anime)
                want.animes_want.remove(anime)
                want.animes_later.remove(anime)
                want.animes_dont.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')

def later_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            want = UsersBack.objects.get(user=request.user)

            if not(UsersBack.objects.filter(user=request.user, animes_later=anime).exists()):
                want.animes_later.add(anime)
                want.animes_done.remove(anime)
                want.animes_now.remove(anime)
                want.animes_want.remove(anime)
                want.animes_dont.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')

def dropped_check(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            want = UsersBack.objects.get(user=request.user)

            if not(UsersBack.objects.filter(user=request.user, animes_dont=anime).exists()):
                want.animes_dont.add(anime)
                want.animes_done.remove(anime)
                want.animes_now.remove(anime)
                want.animes_want.remove(anime)
                want.animes_later.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')


def list(request, slug):
    if request.user.is_authenticated and not request.user.is_anonymous  :
        try:
            user_back = UsersBack.objects.get(is_active=True, user=request.user)
        except:
            raise Http404

        print('not here 1')
        if slug == 'completed':
            animes = user_back.animes_done.all()
            title = 'أنميات تم مشاهدتها'

        elif slug == 'plan-to-watch':
            animes = user_back.animes_want.all()
            title = 'أنميات أرغب بمشاهدتها'

        elif slug == 'watching':
            animes = user_back.animes_now.all()
            title = 'أنميات أشاهدها حاليا'

        elif slug == 'watch-later':
            animes = user_back.animes_later.all()
            title = 'أنميات سأكملها لاحقاً'

        elif slug == 'dropped':
            animes = user_back.animes_dont.all()
            title = 'أنميات لا أرغب بمشاهدتها'
        elif slug == 'favorites':
            animes = user_back.animes_fav.all()
            title = 'أنمياتي المفضلة'
            
        elif slug == 'last_show':
            animes = user_back.last_animes.all()
            title = 'أخر المشاهدات'
            
        else:
            raise Http404

        
        s = 1
        if request.method == 'GET':
            if 'page' in request.GET:
                s = request.GET['page']

        paginator = Paginator(animes, 24)


        try:
            page = paginator.page(s)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        if page.number <= 1:
            page.range = range(page.number, paginator.num_pages+1)[:3]
        elif page.number == 2:
            page.range = range(page.number-1, paginator.num_pages+1)[:4]
        else:
            page.range = range(page.number-2, paginator.num_pages+1)[:5]

        x = {
            'title': title,
            'page': page,
            'domain': get_current_site(request),
            'icon': 'bookmark',
            'title1': 'أنميات',
            'title2': 'أرغب بمشاهدتها',
            'user': user_back
        }

        return render(request, 'news/animes-user.html', x)
    else:
        return redirect('login')


def delete_from_list(request, name):
    try:
        name = name.replace('-', ' ')
        anime = get_object_or_404(Anime, name=name)
    except:
        raise Http404

    if request.user.is_authenticated and not request.user.is_anonymous :
        if request.is_ajax():
            user = UsersBack.objects.get(user=request.user)

            user.animes_want.remove(anime)
            user.animes_done.remove(anime)
            user.animes_dont.remove(anime)
            user.animes_now.remove(anime)
            user.animes_later.remove(anime)

            return JsonResponse()
        raise Http404
    else:
        return redirect('login')


