import os

# Sets environmental variable for django to determine which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spunimusic.settings')

import django
# Imports django project settings
django.setup()
# Performed following initialisation to avoid exception
from spuni.models import Song

def populate():
    # List of songs (as dicts)
    songs = [
        {'name':'White Room',
            'albumArt':'https://m.media-amazon.com/images/I/8177+svLK7L._SS500_.jpg',
            'upvotes':30,
            'artist':'Cream'},
        {'name':'Hurt',
            'albumArt':'https://m.media-amazon.com/images/I/71XA7yLmKsL._SS500_.jpg',
            'upvotes':20,
            'artist':'Johnny Cash'},
        {'name':'Gymnopedie No.1',
            'albumArt':'https://i.scdn.co/image/ab67616d0000b2734ec6176b5c79bcb2a4747ea7',
            'upvotes':100,
            'artist':'Erik Satie'},
        {'name':'Renai Circulation',
            'albumArt':'https://i.scdn.co/image/ab67616d0000b273ea5bdf10f5dff4f60461a493',
            'upvotes':1000,
            'artist':'Kana Hanazawa'},
        {'name':'Never Gonna Give You Up',
            'albumArt':'https://m.media-amazon.com/images/I/7176iTv3geL._SS500_.jpg',
            'upvotes':0,
            'artist':'Rick Astley'}
    ]

    for song in songs:
        add_song(song['name'], song['albumArt'], song['upvotes'], song['artist'])

def add_song(name, albumArt, upvotes, artist):
    s = Song.objects.get_or_create(name=name, albumArt=albumArt, upvotes=upvotes, artist=artist)[0]
    s.save()
    return s


if __name__ == '__main__':
    print('Populating Songs')
    populate()