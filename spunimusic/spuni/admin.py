from django.contrib import admin
from spuni.models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'upvotes', 'artist')

admin.site.register(Song, SongAdmin)