from django.core.management.base import BaseCommand, CommandError
import requests
from pages.models import *
from account.models import *
from pages.resources import *
from django.contrib.auth.models import User
import json
from django.utils import timezone
import time
#from import_export import resources
from django.conf import settings
import os
from pages.serializers import *

def add_episodes():
    # variables
    types = {
    '6': 'الحلقة',
    '7': 'لحلقة خاصة',
    '8': 'الأوفا',
    '9': 'الأونا',
    '10': 'الفلم',
    }
    data = Anime.objects.exclude(anime_days='15')
    url = 'https://animelek.me/anime/'
    url_eps = 'https://animelek.me/episode/'
    line = 0
    w = open('names.txt', 'w', encoding='utf-8')

    # text variables
    ty1 = '''<h3><a style="color:#969696;" href="'''
    t = ty1 + 'https://animelek.me/episode/'
    ln = len(ty1)



    t_eps = '''  <iframe id="Animelek1-episode-iframe"
                                            src="'''
    rt_eps = '''"
                                            frameborder="0" allowfullscreen>'''

    qwe = '<iframe id="Animelek1-episode-iframe" src="'
    wqt = '" frameborder="0" allowfullscreen>'
    ln_eps2 = len(qwe)
    ln_eps = len(t_eps)

    #print(data)
    for dt in data:
        name = dt.name.replace(' ', '-')
        try:
            r = requests.get(f'{url}{name}')
        except:
            print(dt)
            continue
        html = r.text


        s = 0
        nju = 0
        try:
            m = Episodes.objects.filter(name=dt).latest('episode').id
        except:
            m = None

        if m != None:
            typ = str(dt.anime_type.pk)
            s = html.find(f'{types[typ]} {m}')
            if s == -1:
                s = 0



        while s != -1:

            s = html.find(t, s)
            if s == -1:
                break
            s = s+ln

            e = html.find('/">', s)



            hb = html.find('</a></h3>', e+3)

            #w.write(html[s:e] + '\n')
            res = []

            for i in html[e+3:hb]:
                if i.isdigit():
                    res.append(i)
            res = ''.join(res)


            nju+=1

            r_eps = requests.get(html[s:e])
            html_eps = r_eps.text

            s_eps = html_eps.find(t_eps)

            if s_eps == -1:
                s_eps = html_eps.find(qwe)
                if s_eps == -1:
                    continue

                s_eps = s+ln_eps2
                e_eps = html_eps.find(wqt, s_eps)
            else:
                s_eps += ln_eps
                e_eps = html_eps.find(rt_eps, s_eps)

            eps = Episodes(name=dt, episode=res, type_html='iframe', type_episode='url', url=html_eps[s_eps:e_eps]).save()

        line+=1
        print(f'{line}  :  {dt.name} ; {m} ; {nju} ' + '\n')
    w.close()

def animelek_add_episodes() :
    r = requests.get("https://api-dolar-argentina-2.herokuapp.com/animelek/hamzalahyane54@gmail.com/imanelahyane/episodes/")
    js = r.json()['episodes']

    for es in js:
        anime = Anime.objects.get(name=es['name'])
        eps = Episodes( name=anime, episode=es['number'], type_html='iframe', type_episode='url', url=es['url']).save()

    w = open('episodes.json', 'w')
    w.write(json.dumps(js))
    w.close()



from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase


from django.template.loader import get_template

#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.

#from xhtml2pdf import pisa
from django.core.mail import EmailMessage

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()

    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


from urlanime.models import Comment
class Command(BaseCommand):
    help = 'Delete objects older than 10 days'

    def handle(self, *args, **options):
        users = UsersBack.objects.all()
        user = users[0]
        episode = 1
        def delete():
            Comment.objects.all().delete()
            
        def add():
            users = UsersBack.objects.all()
            user = users[0]
            pk = 1
            for i in range(1, 7):
                cm = Comment(content=f"Comment {i} From {user.user.username}", episode=episode, user=user, pk=pk)
                cm.save()
                pk+=1

            cms = Comment.objects.filter(parent=None)

            rps = []
            for rp in cms:
                for us in users[1:]:
                    l = Comment(reply=rp, parent=rp, content='Reply Inside', user=us)
                    l.save()
                    rps.append(l)

            for k in rps:
                for i in users:
                    Comment(parent=k.parent, reply=k, content=f'Reply inside reply', user=i, episode=episode).save()
            


        delete()
        add()
       
        '''
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
        '''

            #time.sleep(60*60)

        self.stdout.write('Deleted objects older than 10 days')










