from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

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
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Song, self).save(*args, **kwargs)

"""
    @brief User model
    @field url photo: Link to user's profile picture
    @field (FK) Song upvotedSongs: Songs upvoted by the user
    Note: ID is automatically implemented by django
    Name and email implemented by User model
"""
class UserProfile(models.Model):
    PHOTO_MAX_LENGTH = 200
    
    # Link currently defined model to user model for auth stuff
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo = models.URLField(max_length=PHOTO_MAX_LENGTH)
    upvotedSongs = models.ForeignKey(Song, on_delete=models.CASCADE)
