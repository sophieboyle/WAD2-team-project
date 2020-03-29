import os

# Sets environmental variable for django to determine which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spunimusic.settings')

import django
# Imports django project settings
django.setup()
# Performed following initialisation to avoid exception
from django.contrib.auth.models import User, UserManager
from spuni.models import Song, UserProfile
from spuni.views import upvote

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
    # Populate song model
    for song in songs:
        add_song(song['name'], song['albumArt'], song['upvotes'], song['artist'])

    # List of user profiles (as dicts)
    users = [
        {'username':'shibe1',
            'password':'iamshibe1',
            'photo':'https://i.pinimg.com/originals/a3/af/17/a3af17efcaf49018a2188c9abb96acc4.png',
            'upvotedSongs':[Song.objects.get(name='Renai Circulation', artist="Kana Hanazawa")]},
        {'username':'shibe2',
            'password':'iamshibe2',
            'photo':'https://66.media.tumblr.com/9aaa6bb6b1d8eef1ad7b7c08fc6d23bf/tumblr_oxz891R1jI1s9dacgo8_250.gifv',
            'upvotedSongs':[Song.objects.get(name='White Room', artist="Cream"), Song.objects.get(name='Renai Circulation', artist="Kana Hanazawa")]}
    ]
    # Populate userProfile
    for user in users:
        add_user(user['username'], user['password'], user['photo'])
        for upvoted_song in user['upvotedSongs']:
            add_relationship(user['username'], upvoted_song)

def add_song(name, albumArt, upvotes, artist):
    s = Song.objects.get_or_create(name=name, albumArt=albumArt, upvotes=upvotes, artist=artist)[0]
    s.save()
    return s

def add_user(username, password, photo):
    user = User.objects.create_user(username=username)
    user.set_password(password)
    user.save()
    u = UserProfile.objects.get_or_create(user=user, photo=photo)
    print(u)
    return u

# Acts as a wrapper for upvote
def add_relationship(username, song):
    upvote({"username": username, "slug": song.slug})

if __name__ == '__main__':
    print('Populating Songs')
    populate()