import spotipy
import unidecode
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def search(term):
    results = sp.search(q=term, limit=20)
    response = {}
    for idx, track in enumerate(results['tracks']['items']):
        song_name = track['name']
        artist_name = track['album']['artists'][0]['name']
        album_art = track['album']['images'][0]['url']
        slug = ''.join(char for char in song_name.replace(" ", "-").lower() if char.isalnum() or char == "-")
        slug = unidecode.unidecode(slug)
        response[idx]= {'name':song_name, 'artist_name':artist_name, 'album_art':album_art, 'slug':slug}
    return response