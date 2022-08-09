
import requests
from django.http import JsonResponse, Http404
from django.contrib import auth
from django.shortcuts import render, redirect
from pages.models import *
from account.models import *

from django.utils import timezone


from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
from django.conf import settings
from pages.serializers import *
from pages.resources import *
import json

dayss = {
    '0': '14',
    '6': '13',
    '5': '12',
    '4': '11',
    '3': '10',
    '2': '9',
    '1': '8',
}



def check_user(request, user, passw, js=True):
    try:
        user = auth.authenticate(username=user, password=passw)
        if user == None:
            raise Http404

        if user.is_superuser == True :
            if js:
                return JsonResponse({'user': 'yes'})
            return True
        else:
            raise Http404
    except:
        raise Http404

def animelek_episodes(request, user, passw):
    if check_user(request, user, passw, False) == True:
        dt = timezone.now()
        day = dayss[dt.strftime('%w')]

        state = AnimeState.objects.get(name='مستمر')
        anime = Anime.objects.filter(anime_state=state)
        animes = []
        for i in anime:
            out = {}
            out['name'] = i.name
            out['type'] = str(i.anime_type.pk)
            try:
                out['max_eps'] = Episodes.objects.filter(name=i).latest('id').episode
            except:
                out['max_eps'] = None
            animes.append(out)

        return JsonResponse({'animes': animes})


def get_animes(request, user, passw):
    if check_user(request, user, passw, False) == True:
        anime = Anime.objects.all()
        out = {}
        for i in anime:
            out[i.name.replace(' ', '-')] = ''

        return JsonResponse({'animes': out})


from tablib import Dataset


def to(n):
    res = []

    while n != 0:
        if n%2 == 0:
            res.append('0')
        else:
            res.append('1')
        n = n//2

    return ''.join(res[::-1])




@api_view(['GET', 'POST'])
def animelek_insert_animes(request, user, passw):
    try:
        user = auth.authenticate(username=user, password=passw)
        path = settings.BASE_DIR
        if user.is_superuser:
            try:
                try:
                    max_id = Anime.objects.latest('pk').id+1
                except:
                    max_id = 1

                classes = AnimeClass.objects.all()
                anime_class = {}
                for i in classes:
                    anime_class[str(i.name)] = i.pk

                animes_date = AnimeDate.objects.all()
                anime_date = {}
                for i in animes_date:
                    anime_date[str(i.name)] = i.pk

                ln = len(request.data)

                for i in range(ln):
                    nb = to(max_id)
                    with open(os.path.join(path, f'media/photos/anime/{nb}.png'), 'wb') as f:
                        f.write(base64.b64decode(request.data[i]['image_anime']))

                    request.data[i]['image_anime'] = f'photos/anime/{nb}.png'
                    request.data[i]['anime_date'] = anime_date[str(request.data[i]['anime_date'])]

                    #request.data[i]['anime_class'] = anime_class
                    if len(request.data[i]['anime_class']) == 0:
                        ty1 = []
                    else:
                        ty1 = request.data[i]['anime_class'].split(',')

                    cls = []

                    for cl in ty1:
                        cls.append(str(anime_class[cl]))

                    request.data[i]['anime_class'] = ','.join(cls)


                    request.data[i]['pk'] = max_id
                    max_id +=1

                person_resource = AnimeResource()
                dataset = Dataset()

                imported_data = dataset.load(f'{request.data}')
                result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

                if not result.has_errors():
                    person_resource.import_data(dataset, dry_run=False)  # Actually import now

                return Response({'animes': f'{request.data}'})

            except:
                return redirect('index')
        else:
            return redirect('index')
    except:
        return redirect('index')



@api_view(['GET', 'POST'])
def animelek_insert_episodes(request, user, passw):
    try:
        user = auth.authenticate(username=user, password=passw)
        path = settings.BASE_DIR
        if user.is_superuser:
            try:

                d = {}
                animes = Anime.objects.all()
                for i in animes:
                    d[i.name] = i

                js = request.data
                for es in js:
                    anime = d[es['name']]
                    if not (Episodes.objects.filter(name=anime, episode=es['number']).exists()):
                        eps = Episodes(name=anime, episode=es['number'])
                        eps.save()
                        for srv in es['srvs']:

                            if not(Server.objects.filter(episode=eps, name=srv['name']).exists()):

                                s = Server(episode=eps, name=srv['name'], lien=srv['lien']).save()


                        for dow in es['dows']:
                            if not(Download.objects.filter(episode=eps, name=dow['name']).exists()):
                                s = Download(episode=eps, name=dow['name'], lien=dow['lien']).save()




                return Response({'episodes': js})

            except:
                return redirect('index')
        else:
            return redirect('index')
    except:
        return redirect('index')


"""
def export(request, user, passw):
    if check_user(request, user, passw, False) == True:
        path = os.path.join(settings.BASE_DIR, 'data')

        # animes
        #print("start")
        # animes
        data_animes = AnimeSerializer(Anime.objects.all())

        animes = open(f'{path}/animes.json', 'w', encoding='utf-8')
        animes.write(str(json.dumps(data_animes.data)))
        animes.close()
        #print("success Anime")

        # Episodes
        data_episodes = EpisodesSerializer(Episodes.objects.all())

        episodes = open(f'{path}/episodes.json', 'w', encoding='utf-8')
        episodes.write(str(json.dumps(data_episodes.data)))
        episodes.close()

        #print("success Episodes")
        # anime_class
        data_anime_class = AnimeClassSerializer(AnimeClass.objects.all())

        anime_class = open(f'{path}/class.json', 'w', encoding='utf-8')
        anime_class.write(str(json.dumps(data_anime_class.data)))
        anime_class.close()

        #print("success anime_class")
        # state
        data_state = AnimeStateSerializer(AnimeState.objects.all())

        state = open(f'{path}/state.json', 'w', encoding='utf-8')
        state.write(str(json.dumps(data_state.data)))
        state.close()

        #print("success state")
        # anime_type
        data_anime_type = AnimeTypeSerializer(AnimeType.objects.all())

        anime_type = open(f'{path}/type.json', 'w', encoding='utf-8')
        anime_type.write(str(json.dumps(data_anime_type.data)))
        anime_type.close()

        #print("success anime_type")
        # days
        data_days = AnimeDaysSerializer(AnimeDays.objects.all())

        days = open(f'{path}/days.json', 'w', encoding='utf-8')
        days.write(str(json.dumps(data_days.data)))
        days.close()

        #print("success days")
        # date
        data_date = AnimeDateSerializer(AnimeDate.objects.all())

        date = open(f'{path}/date.json', 'w', encoding='utf-8')
        date.write(str(json.dumps(data_date.data)))
        date.close()

        #print("success date")




        return JsonResponse({'dfd': 'gfgfg'})
        ##print("success date")

"""







