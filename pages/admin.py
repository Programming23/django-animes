from django.contrib import admin
from .models import Anime, AnimeClass, AnimeDate, AnimeDays, AnimeState, AnimeType, Episodes, Server, Download
from import_export import resources
from import_export.admin import ImportExportModelAdmin




@admin.register(Anime)
class AnimeAdmin(ImportExportModelAdmin):
    search_fields = ['name', 'story']
    pass


@admin.register(AnimeType)
class AnimeTypeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name',  'publish_date')


@admin.register(AnimeDate)
class AnimeDateAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name',  'publish_date')


@admin.register(AnimeClass)
class AnimeClassAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name',  'publish_date')


@admin.register(AnimeState)
class AnimeStateAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    list_display = ('pk', 'name',  'publish_date')


@admin.register(AnimeDays)
class AnimeDaysAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'name',  'publish_date')
    search_fields = ['name']
    


@admin.register(Episodes)
class EpisodesAdmin(ImportExportModelAdmin):
    list_display = ('name', 'episode', 'publish_date')
    search_fields = ['episode']
    

@admin.register(Server)
class ServerAdmin(ImportExportModelAdmin):
    list_display = ('id','episode', 'name', 'publish_date')
    search_fields = ('lien', 'name')

@admin.register(Download)
class DownloadAdmin(ImportExportModelAdmin):
    list_display = ('id','episode', 'name', 'publish_date')
    search_fields = ('lien', 'name')

