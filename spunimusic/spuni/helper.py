"""
    Contains functions to be used by frontend
    Used to modify database when upvoting songs
"""
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def upvote(username, songname):
    # Get objects from database for given parameters
    u = UserProfile.objects.get(user=User.objects.get(username=username))
    s = Song.objects.get(name=songname)
    # Check if the user has already upvoted this song
    try:
        upvSong = u.upvotedSongs.get(name=songname)
    except ObjectDoesNotExist:
        # If not, upvote
        upvSong = u.upvotedSongs.add(s)