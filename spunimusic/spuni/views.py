from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from spuni.models import Song
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout as auth_logout

# View to show pages for a given song
def show_song(request, song_name_slug):
    context_dict = {}
    # Song has been found and added to context
    try:
        song = Song.objects.get(slug=song_name_slug)
        context_dict['song'] = song
    # Song by that ID was not found
    except Song.DoesNotExist:
        context_dict['song'] = None
    return render(request, 'song.html', context=context_dict) 

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        return render(request, 'userprofile/index.html', {'username':username})
    else:
        return render(request, 'index.html')
    

def logout(request):
    auth_logout(request)
    return render('index.html')