import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def search(term):
    results = sp.search(q=term, limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
