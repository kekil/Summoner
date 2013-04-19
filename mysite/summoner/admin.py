from django.contrib import admin
from summoner.models import Summoner, Match

class MatchesInline(admin.TabularInline):
    model = Match

class SummonerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    inlines= [MatchesInline]
    list_display = ['name']
    list_filter = ['name']
    search_fields= ['name']

admin.site.register(Summoner, SummonerAdmin)
