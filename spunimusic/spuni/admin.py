from django.contrib import admin
from spuni.models import Song, UserProfile

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'upvotes', 'artist')


admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile)