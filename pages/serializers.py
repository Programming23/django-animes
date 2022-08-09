from rest_framework import serializers
from pages.models import *
from account.models import *

class AnimeDaysSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)



class AnimeTypeSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)


class AnimeStateSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)


class AnimeDateSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)


class EpisodesSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name.pk
            res['episode'] = i.episode
            res['url'] = str(i.url)
            res['video'] = str(i.video)
            res['type_html'] = str(i.type_html)
            res['type_episode'] = str(i.type_episode)
            res['count_watching'] = i.count_watching
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)





class AnimeClassSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)


class AnimeSerializer():
    data = []

    def __init__(self, data):
        self.data = []
        for i in data:
            res = {}
            res['id'] = i.id
            res['name'] = i.name
            res['story'] = i.story
            res['anime_type'] = i.anime_type.pk
            res['anime_state'] = i.anime_state.pk
            res['anime_days'] = i.anime_days.pk
            res['anime_date'] = i.anime_date.pk
            res['number_episodes'] = i.number_episodes

            cls = i.anime_class.all()
            anime_class = []
            for cl in cls:
                anime_class.append(str(cl.pk))

            res['anime_class'] = ','.join(anime_class)
            res['image_anime'] = str(i.image_anime)

            res['publish_date'] = str(i.publish_date)[:-6]
            self.data.append(res)











