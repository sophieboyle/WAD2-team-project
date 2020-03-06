from django.db import models
from spunimusic.spuni.models import Song

"""
    @brief User model
    @field string name: User's username
    @field email email: User's email
    @field url photo: Link to user's profile picture
    @field (FK) Song upvotedSongs: Songs upvoted by the user
    Note: ID is automatically implemented by django
"""
class User(models.Model):
    NAME_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 254
    PHOTO_MAX_LENGTH = 200
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    photo = models.URLField(max_length=PHOTO_MAX_LENGTH)
    upvotedSongs = models.ForeignKey(Song)
