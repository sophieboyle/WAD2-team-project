"""
    Contains functions to be used by frontend
    Used to modify database when upvoting songs
"""
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

"""
    @brief Given a username and songname, either creates
           a new relationship or leaves the relationship
           unchanged. Also increments song's upvote value
    @param username: User's username as a string
    @param songname: Songname as a string (not a slug) 
"""
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
        s.upvotes += 1
        s.save()