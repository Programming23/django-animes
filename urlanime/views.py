
from django.shortcuts import render, get_object_or_404, redirect
from pages.models import Anime, Episodes, Server, Download
from django.http import *
from account.models import UsersBack,ipAdress
from django.contrib.sites.shortcuts import get_current_site
from pages.views import get_client_ip



# Create your views here.
def anime(request, slug):
    try:
        anime = get_object_or_404(Anime, name=slug.replace('-',' '))
    except:
        raise Http404

    domain = get_current_site(request)
    class_fav = ''
    episodes = Episodes.objects.filter(name=anime).order_by('id')
    class_done = ''
    class_want = ''
    class_dont = ''
    class_now = ''
    class_later = ''
    close = ''

    ls = False
    if request.user.is_authenticated:
        if UsersBack.objects.filter(user=request.user, animes_fav=anime).exists():
            class_fav = 'background: #ffcece;'

        if UsersBack.objects.filter(user=request.user, animes_done=anime).exists():
            class_done = 'background: #ffe4e4;'

        elif UsersBack.objects.filter(user=request.user, animes_want=anime).exists():
            class_want = 'background: #ffe4e4;'

        elif UsersBack.objects.filter(user=request.user, animes_now=anime).exists():
            class_now = 'background: #ffe4e4;'

        elif UsersBack.objects.filter(user=request.user, animes_later=anime).exists():
            class_later = 'background: #ffe4e4;'

        elif UsersBack.objects.filter(user=request.user, animes_dont=anime).exists():
            class_dont = 'background: #ffe4e4;'
        else:
            close = 'display: none;'



    genre = anime.anime_class.all()
    


    x = {
        'anime' : anime,
        'class' : genre,
        'title' : anime.name.title(),
        'episodes': episodes,
        'class_fav': class_fav,
        'class_dont': class_dont,
        'class_now': class_now,
        'class_later': class_later,
        'class_done': class_done,
        'class_want': class_want,
        'domain': domain,
    }


    if request.user.is_authenticated:
        x['user'] = request.user.user
        x['close'] = close

    return render(request, 'news/anime.html', x)

def watch(request, name, typ, episode):
    try:
        name = name.replace('-',' ')
        anime = Anime.objects.get(name=name)
        
        if anime.anime_type.type_url != typ:
            raise Http404
        
        
        episode = Episodes.objects.get(name=anime, episode=episode)
    except:
        raise Http404

    ip = get_client_ip(request)
    try:
        aip = ipAdress.objects.get(ip=ip)
        
        if not(ipAdress.objects.filter(ip=aip.ip, eps_show=episode).exists()):
            aip.eps_show.add(episode)
    except :
        aip = ipAdress(ip=ip)
        aip.eps_show.add(episode)
      
   
    episode.save()
    aip.save()
    

    domain = get_current_site(request)
    episodes = Episodes.objects.filter(name=episode.name).order_by('id')

    #episode = Episodes.objects.get(name=anime, episode=str(eps_num))
    episode.title = episode.name.name.title()
    episode.type = episode.name.anime_type.type
    m = 'hide'
    n = 'hide'

    nex = episodes.filter(pk__gt=int(episode.pk))
    prvg = episodes.filter(pk__lt=int(episode.pk))

    servers = Server.objects.filter(episode=episode)
    dows = Download.objects.filter(episode=episode)
    
    if len(nex) > 0:
        n = nex[0]

    if len(prvg) > 0:
        m = list(prvg)[-1]

    
    
    x = {
        'dows': dows,
        'servers': servers,
        'episode': episode,
        'episodes': episodes,
        'prv_hide': m,
        'next_hide': n,
        'domain': domain,
    }
    
    if request.user.is_authenticated:
        
        user_back = UsersBack.objects.get(user=request.user,  is_active=True)
        x['user'] = user_back
        try:
            last = UsersBack.objects.get(user=request.user ,is_active=True, last_animes=episode.name)
            last.last_animes.remove(episode.name)
            last.save()
        except:
            pass
        
        last = user_back.last_animes.add(episode.name)
        
    
     
    return render(request, 'news/watch.html', x)




def error404(request, exception):
    return redirect('index')

def error500(request, *args, **argv):
    return render(request, 'errors/error500.html')

def error403(request, *args, **argv):
    return render(request, 'errors/error403.html')