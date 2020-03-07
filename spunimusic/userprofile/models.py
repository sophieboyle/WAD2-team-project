from django.db import models
from spuni.models import Song
from django.contrib.auth.models import User

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
