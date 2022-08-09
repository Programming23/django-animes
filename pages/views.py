
from django.shortcuts import redirect, render, get_object_or_404
from .models import AnimeDays, AnimeState, AnimeClass, AnimeDate, AnimeType, Anime, Episodes
from account.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import  force_bytes, force_str, force_text
from pages.forms import *
import os
#from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import auth

type_real = {
    'تلفزيون' : 'الحلقة',
    'الحلقة الخاصة': 'حلقة خاصة',
    'أوفا': 'الأوفا',
    'أونا': 'الأونا',
    'فيلم': 'الفيلم'
}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def comments(request):

    from urlanime.models import Comment

    
    if request.method == 'DELETE':
        try:
            pk = request.headers.get('pk')
            cm = Comment.objects.get(pk=pk)
            if cm.user == request.user.user:
                cm.delete()
                
        except:
            pass

    episode = 1
    if request.method == 'POST':
        if 'parent' in request.POST:
            try:
                parent = request.POST['parent']
                reply = request.POST['reply']
                content = request.POST['content']
                reply = Comment.objects.get(pk=reply)
                parent = Comment.objects.get(pk=parent)
                Comment(content=content, episode=episode, parent=parent, reply=reply, user=request.user.user).save()
            except:
                pass

        elif 'content' in request.POST:
                content = request.POST['content']
                Comment(reply=None,parent=None, user=request.user.user, episode=episode, content=content).save()
       


    x = {
        'comments': Comment.objects.filter(parent=None)
    }
    return render(request, 'news/comments.html', x)


def index(request):
    
    ip = get_client_ip(request)

    try:
        aip = ipAdress.objects.get(ip=ip)
    except :
        aip = ipAdress(ip=ip)
        aip.save()


    domain = get_current_site(request)
    if len(Domain.objects.all()) == 0:
        dm = Domain(domain=domain).save()

    episodes = Episodes.objects.all()[:24]
    animes = Anime.objects.all()[:24]


    x = {
        'episodes': episodes,
        'animes_search': animes,
        'domain': domain,
    }
    if request.user.is_authenticated:
        x['user'] = request.user.user

    
    return render(request, 'news/index.html', x)


def edit_profile(request):
    ip = get_client_ip(request)

    try:
        aip = ipAdress.objects.get(ip=ip)
    except :
        aip = ipAdress(ip=ip)
        aip.save()

    if not(request.user.is_authenticated):
        return redirect('login')


    profile = request.user
    username = profile.username
    bio = profile.user.bio
    social_twitter = profile.user.social_twitter
    social_github = profile.user.social_github
    social_instagram = profile.user.social_instagram
    social_website = profile.user.social_website
    profile_image = profile.user.profile_image
    notification = ''
    public = ''
    if profile.user.notification == True:
        notification = 'checked'
    if profile.user.information_public == True:
        public = 'checked'
    error = ''


    if request.method == 'POST' :
        if 'username' in request.POST:
            usrn = request.POST['username']
            if usrn != username:

                if len(usrn) < 8:
                    error = 'اسم المستخدم يجب أن يكون أكثر من 8 أحرف'
                elif usrn.find(' ') != -1:
                    error = 'اسم المستخدم يجب ألا يحتوي على مسافات'
                elif User.objects.filter(username=usrn).exists():
                    error = 'اسم المستخدم موجود مسبقاً'
                else:
                    username = usrn
                    profile.username = usrn
        profile.save()
        user_back = UsersBack.objects.get(user=profile)
        if error == '' and request.FILES:
            if not ('profile_image' in request.FILES) :
                error = 'خطأ'
            else:
                user_back.profile_image = request.FILES['profile_image']
                user_back.profile_image.name = str(request.user.pk) + '.png'

        if error == '':

            if 'bio' in request.POST:
                bio = request.POST['bio']
                user_back.bio = bio

            if 'social_github'  in request.POST:
                social_github = request.POST['social_github']
                user_back.social_github = social_github

            if 'social_website' in request.POST:
                social_website = request.POST['social_website']
                user_back.social_website = social_website

            if 'social_twitter'  in request.POST:
                social_twitter = request.POST['social_twitter']
                user_back.social_twitter = social_twitter

            if 'social_instagram'  in request.POST:
                social_instagram = request.POST['social_instagram']
                user_back.social_instagram = social_instagram

            if 'notification' in request.POST:
                notification = request.POST['notification']
                if notification == 'on':
                    user_back.notification = True
                else:
                    user_back.notification = False
            else:
                user_back.notification = False

            if 'public' in request.POST:
                information_public = request.POST['public']
                if information_public == 'on':
                    user_back.information_public = True
                else:
                    user_back.information_public = False
            else:
                    user_back.information_public = False


            user_back.save()


            return redirect('profile')





    context = {
        'value_username': username,
        'value_bio': bio,
        'value_instagram': social_instagram,
        'value_github': social_github,
        'value_website': social_website,
        'value_twitter': social_twitter,
        'profile_image': profile_image,
        'error': error,
        'notification': notification,
        'public': public,
        }
    return render(request, 'users/edit-profile.html', context)

# list-anime
def list_anime(request):
    ip = get_client_ip(request)

    try:
        aip = ipAdress.objects.get(ip=ip)
    except :
        aip = ipAdress(ip=ip)
        aip.save()

    s = 1
    title = 'الأنميات'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()
    animes = Anime.objects.all()
    sort_by = ['name', 'publish_date', 'anime_date']
    sort_sys = ['-', '+']
    def_sort_by = 'publish_date'
    def_sort_sys = '-'
    
    

    genres = []
    seasons = []
    types = []
    state = []

    if request.method == 'GET':
        w = open('test.txt', 'w')
        w.write(str(request.GET))
        w.close()

        if 'page' in request.GET:
            s = request.GET['page']

        if 's' in request.GET:
            name = request.GET['s']
            try:
                animes = animes.filter(name__icontains=name)
            except:
                pass

        if 'sort_by' in request.GET and request.GET['sort_by'] in sort_by:
            def_sort_by = request.GET['sort_by']

        if 'sort_sys' in request.GET and request.GET['sort_sys'] in sort_sys:
            if request.GET['sort_sys'] == '+':
                def_sort_sys = ''
            else:
                def_sort_sys = request.GET['sort_sys']
        
        if 'types' in request.GET:
            try:
                types = request.GET.getlist('types')
                animes = animes.filter(anime_type__name__in=types)
            except:
                pass

        if 'genres' in request.GET:
            try:
                genres = request.GET.getlist('genres')
                animes = animes.filter(anime_class__name__in=genres)
            except:
                pass      

        if 'seasons' in request.GET:
            try:
                seasons = request.GET.getlist('seasons')
                animes = animes.filter(anime_date__name__in=seasons)
            except:
                pass    

        if 'state' in request.GET:
            try:
                state = request.GET.getlist('state')
                animes = animes.filter(anime_state__name__in=state)
            except:
                pass     
  
    animes = animes.order_by(f'{def_sort_sys}{def_sort_by}')
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




    get = ''
    path = request.META['QUERY_STRING']
    index_page = path.find('page')
    if index_page == -1:
        get = path
    else:
        end = path.find('&', index_page)
        if end == -1:
            get = path[:index_page]
        else:
            get = path[:index_page] + path[index_page+1:]

    if get != '' and get[-1] != '&':
        get +='&'

    x = {
        'title': title,
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'sort_by': sort_by,
        'def_sort_by': def_sort_by,
        'def_sort_sys': def_sort_sys,
        'genres': genres,
        'types': types,
        'state': state,
        'seasons': seasons,
        'page': page,
        'urlpath': f'قائمة افلام وانميات  مترجمة اون لاين',
        'domain': get_current_site(request),
        'get': get
    }
    if request.user.is_authenticated:
        x['user'] = request.user.user

    return render(request, 'news/list-anime.html', x)

'''
# anime-genre ... => ht
def ht(request, name, slug):
    if name == 'anime-genre' or name == 'anime-state' or name == 'anime-type' or name == 'anime-season':
        s = 1
        anime_type = AnimeType.objects.all()
        anime_state = AnimeState.objects.all()
        anime_date = AnimeDate.objects.all()
        anime_class = AnimeClass.objects.all()
        animes = Anime.objects.all()


        slug_rep = slug.replace('-', ' ')
        if name == 'anime-state':
            cls = get_object_or_404(AnimeState, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_state=cls)

            title = f'حالة الأنمي [ {cls.name} ]'


        elif name == 'anime-genre':
            cls = get_object_or_404(AnimeClass, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_class=cls)

            title = f'تصنيف الأنمي [ {cls.name} ]'

        elif name == 'anime-type':
            cls = get_object_or_404(AnimeType, name=slug_rep)
            urlpath = f'{slug_rep}'
            animes = animes.filter(anime_type=cls)
            title = f'نوع الأنمي [ {cls.name} ]'

        elif name == 'anime-season':
            cls = get_object_or_404(AnimeDate, name=slug)
            urlpath = f'موسم {slug_rep}'
            animes = animes.filter(anime_date=cls)

            title = f'الموسم [ {cls.name} ]'

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
            'anime_type': anime_type,
            'anime_state': anime_state,
            'anime_date': anime_date,
            'anime_class': anime_class,
            'page': page,
            'urlpath': f'قائمة افلام وانميات {urlpath} مترجمة اون لاين',
            'domain': get_current_site(request)

        }





        return render(request, 'news/list-anime.html', x)
    else:
        return render(request, 'pages/error404.html')

'''

# episode
def episode(request):
    ip = get_client_ip(request)

    try:
        aip = ipAdress.objects.get(ip=ip)
    except :
        aip = ipAdress(ip=ip)
        aip.save()

    s = 1
    title = 'حلقات الأنمي'
    episode = Episodes.objects.all()


    if request.method == 'GET':
        if 'page' in request.GET:
            s = request.GET['page']


    paginator = Paginator(episode, 24)

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
        'page': page,
        'ul_hide' : 'hide',
        'title': title,
    }

    if request.user.is_authenticated:
        x['user'] = request.user.user
    return render(request, 'news/episode.html', x)

'''
# search

def search(request):
    s = 1
    title = 'نتائج البحث عن [  ]'
    anime_type = AnimeType.objects.all()
    anime_state = AnimeState.objects.all()
    anime_date = AnimeDate.objects.all()
    anime_class = AnimeClass.objects.all()
    animes = Anime.objects.all()
    search = 'hide'
    sr = ''



    if request.method == 'GET':
        if 'page' in request.GET:
            s = request.GET['page']
        if 's' in request.GET:
            sr = request.GET['s']
            search = 'show'
            title = f'نتائج البحث عن [ {sr} ]'
            animes = animes.filter(name__icontains=sr)
            #sr = sr.replace(' ', '+')

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
        'anime_type': anime_type,
        'anime_state': anime_state,
        'anime_date': anime_date,
        'anime_class': anime_class,
        'page': page,
        'search': search,
        'search_text': sr.replace(' ','+'),
        'domain': get_current_site(request),
        'urlpath': f'نتائج البحث عن {sr}',
        'domain': get_current_site(request),
    }


    return render(request, 'news/list-anime.html', x)
'''
def days_anime(request):
    ip = get_client_ip(request)

    try:
        aip = ipAdress.objects.get(ip=ip)
    except :
        aip = ipAdress(ip=ip)
        aip.save()

    days = AnimeDays.objects.all()[:7]
    state = AnimeState.objects.get(name='مستمر')

    for i in days:

        i.animes = Anime.objects.filter(anime_days=i, anime_state=state)



    x = {
        'days': days,
        'domain': get_current_site(request),
    }
    if request.user.is_authenticated:
        x['user'] = request.user.user

    return render(request, 'news/days_anime.html', x)


def media(request, path):
    raise Http404

def page_reset(request):
    return redirect('index')



