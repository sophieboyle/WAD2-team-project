from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from spuni.models import Song
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# View to show pages for a given song
def show_song(request, song_name_slug):
    context_dict = {}
    # Song has been found and added to context
    try:
        song = Song.objects.get(slug=song_name_slug)
        context_dict['song'] = song
    # Song by that slug was not found
    except Song.DoesNotExist:
        context_dict['song'] = None
    return render(request, 'spuni/song.html', context=context_dict) 