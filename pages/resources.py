from pages.models import *
from account.models import *
from import_export import resources
from django.contrib.auth.models import User

class AnimeResource(resources.ModelResource):
    class Meta:
        model = Anime

class EpisodesResource(resources.ModelResource):
    class Meta:
        model = Episodes

class AnimeClassResource(resources.ModelResource):
    class Meta:
        model = AnimeClass

class AnimeTypeResource(resources.ModelResource):
    class Meta:
        model = AnimeType

class AnimeStateResource(resources.ModelResource):
    class Meta:
        model = AnimeState

class AnimeDaysResource(resources.ModelResource):
    class Meta:
        model = AnimeDays

class AnimeDateResource(resources.ModelResource):
    class Meta:
        model = AnimeDate

class UserResource(resources.ModelResource):
    class Meta:
        model = User

class UsersBackResource(resources.ModelResource):
    class Meta:
        model = UsersBack

