# Spuni - Crowd sourcing playlists
## Introduction
- The objective of our application is to compile a global user playlist, consisting of the top voted songs. Individual users will be allowed to search for, add and upvote songs.​

- Users will also have a personally-compiled playlist available on their profiles, consisting of the songs that they have personally upvoted.​

- This functionality is provided by interfacing the application with the Spotify python API found here: https://developer.spotify.com/documentation/web-api/​

## Development Build
1. Make virtual environment.

    `mkvirtualenv spunienv`
2. Activate environment.

    `workon spunienv`
3. Install requirements.

    `pip install --user --requirement requirements.txt`
4. If you're using VSCode:

    In VSCode <kbd>cmd/ctrl</kbd> + <kbd>shift</kbd> + <kbd>P</kbd>.

    Select Python: Select interpreter.

    Then select spunienv.






## General Notes
Spotify redirect URI: http://localhost:8000/social/complete/spotify/

Make sure while in development, you use localhost and not 127.0.0.1 because Spotify won't be able to redirect otherwise.

## Helpful Docs
- https://kholinlabs.com/django-authentication-via-google-deezer-and-spotify
- https://python-social-auth.readthedocs.io/

## TODO List
- [x] Spotify login.
- [] Basic web pages. i.e Home, Profile, etc.

