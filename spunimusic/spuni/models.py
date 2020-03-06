from django.db import models

"""
    @brief Song model
    @field string name: Name of the song
    @field int upvotes: Number of upvotes the song has
    @field string artist: The name of the song's artist
    Note: ID is automatically implemented by django
"""
class Song(models.Model):
    NAME_MAX_LENGTH = 128
    ARTIST_MAX_LENGTH = 128
    ALBUM_ART_MAX_LENGTH = 200

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    albumArt = models.URLField(max_length=ALBUM_ART_MAX_LENGTH)
    upvotes = models.IntegerField(default = 0)
    artist = models.CharField(max_length=ARTIST_MAX_LENGTH)
