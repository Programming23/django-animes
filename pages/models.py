
from django.db import models
from django.db.models.base import Model
from datetime import datetime
from django.utils import timezone
import pytz

from django.core.validators import FileExtensionValidator
from django.utils.encoding import  force_bytes, force_str, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your models here.

type_real = {
    'تلفزيون' : 'الحلقة',
    'حلقة خاصة': 'الحلقة الخاصة',
    'أوفا': 'الأوفا',
    'أونا': 'الأونا',
    'فيلم': 'الفيلم'
}
type_urls = {
    'تلفزيون' : 'episode',
    'حلقة خاصة': 'special',
    'أوفا': 'ova',
    'أونا': 'ona',
    'فيلم': 'movie'
}

class AnimeType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.name

    @property
    def type(self):
        data = type_real[self.name]

        return data

    @property
    def type_url(self):
        data = type_urls[self.name]

        return data


    @property
    def url(self):
        data = self.name.replace(' ', '+')

        return data




class AnimeState(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )


    def __str__(self):
        return self.name

    @property
    def url(self):
        data = self.name.replace(' ', '+')

        return data




class AnimeClass(models.Model):
    name = models.CharField(unique=True, max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name

    @property
    def url(self):
        data = self.name.replace(' ', '+')

        return data

class AnimeDate(models.Model):
    name = models.IntegerField(unique=True)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'



class AnimeDays(models.Model):
    name = models.CharField(unique=True ,max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.name



class Anime(models.Model):
    name = models.CharField(unique=True, max_length=150)

    story = models.TextField( default='')

    image_anime = models.ImageField( upload_to='photos/anime', default='')

    anime_type = models.ForeignKey(AnimeType, on_delete=models.CASCADE)

    anime_state = models.ForeignKey(AnimeState, on_delete=models.CASCADE)

    anime_date = models.ForeignKey(AnimeDate, on_delete=models.CASCADE)

    anime_days = models.ForeignKey(AnimeDays, on_delete=models.CASCADE)

    anime_class = models.ManyToManyField(AnimeClass)

    number_episodes = models.CharField( max_length=50)

    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.name

    @property
    def want_show(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_want=self).count

        return data

    @property
    def done_show(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_done=self).count

        return data

    @property
    def now_show(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_now=self).count

        return data

    @property
    def fav_count(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_fav=self).count

        return data

    @property
    def dont_show(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_dont=self).count

        return data

    @property
    def later_show(self):
        from account.models import UsersBack
        data = UsersBack.objects.filter(animes_later=self).count

        return data

    @property
    def url_anime(self):
        data = self.name.replace(' ', '-')

        return data


class Episodes(models.Model):
    choices = (
        ('video', 'video'),
        ('url', 'url')
    )

    choices_html = (
        ('video', 'video'),
        ('iframe', 'iframe')
    )

    name = models.ForeignKey(Anime, on_delete=models.CASCADE)
    episode = models.CharField(max_length=30)
    #url = models.URLField( max_length=200, default='', blank=True)
    #video = models.FileField(blank=True, upload_to='video/anime/%Y/%m/%d', max_length=500, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    publish_date = models.DateTimeField( default=timezone.now )

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return f'{self.name} {self.episode}'

    @property
    def url_episode(self):
        data = f'أنمي-{self.name.url_anime}-{self.name.anime_type.type}-{self.episode}'

        return data

    @property
    def count_watching(self):
        from account.models import ipAdress
        data = ipAdress.objects.filter(eps_show=self).count

        return data


class Server(models.Model):
    episode = models.ForeignKey(Episodes, on_delete=models.CASCADE)
    lien = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'{self.episode}'


class Download(models.Model):
    episode = models.ForeignKey(Episodes, on_delete=models.CASCADE)
    lien = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    publish_date = models.DateTimeField( default=timezone.now )

    def __str__(self):
        return f'{self.episode}'

        