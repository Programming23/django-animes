from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UsersBack, Tokens, Domain, ipAdress
# Register your models here.
    
@admin.register(UsersBack)
class AnimeAdmin(ImportExportModelAdmin):
    pass

@admin.register(Tokens)
class AnimeAdmin(ImportExportModelAdmin):
    pass

@admin.register(Domain)
class AnimeAdmin(ImportExportModelAdmin):
    pass

@admin.register(ipAdress)
class AnimeAdmin(ImportExportModelAdmin):
    pass
