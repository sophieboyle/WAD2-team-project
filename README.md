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




## Stuff for spotipy

- In your terminal do the following:

```
export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here

// on Windows, use `SET` instead of `export`
```
- API keys can be found in the one page submission document.

## Running the Server

- Initialise the database.

```
cd spunimusic
python manage.py migrate
```

- Populate the database with test data.

```
python populate_spuni.py
```

- Run the server

```
python manage.py runserver
```

## General Notes
Spotify redirect URI: http://localhost:8000/social/complete/spotify/

Make sure while in development, you use localhost and not 127.0.0.1 because Spotify won't be able to redirect otherwise.

## Technologies Used

- Django 3.0.3 
https://www.djangoproject.com/

- Spotipy
https://spotipy.readthedocs.io/en/2.9.0/

- Crispy Forms
https://django-crispy-forms.readthedocs.io/en/latest/

- Bootstrap
https://getbootstrap.com/

- SQLite
https://www.sqlite.org/index.html

- Google Fonts
https://fonts.google.com/

- Ajax
https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX
