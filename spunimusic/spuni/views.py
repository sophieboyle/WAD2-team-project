from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from spuni.models import Song, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import logout as auth_logout
from spuni.forms import UserForm, UserProfileForm, SongForm, LoginForm
from spuni.spotifyapi import search
from django.core.exceptions import ObjectDoesNotExist

"""
    @brief Shows the song details for the given song on song.html
    @param request
    @param String song_name_slug: Slugified song name
"""
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


"""
    @brief Shows index view on index.html
    @param request
    @return render of index with a context dictionary containing 
            songs to display.
"""
def index(request):
    song_list = Song.objects.order_by('-upvotes')
    context_dict = {'songs': song_list}

    if request.user.is_authenticated:
        username = request.user.username
        context_dict["username"] = username
        
        return render(request, 'index.html', context_dict)
    else:
        return render(request, 'index.html', context_dict)
    

"""
    @brief Logout view
    @param request
    @return Redirects to index
"""
def logout(request):
    auth_logout(request)
    return index(request)


"""
    @brief Shows the registration forms for new users to register
    @param request
    @return Render of the register page with the context dict containing
            the userform, profileform, and also whether or not the registration
            was successful.
"""
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Hash passwd and save
            user.set_password(user.password)
            user.save()

            # Set up userProfile stuff without committing to db
            # Avoids integrity issues
            profile = profile_form.save(commit=False)
            profile.user = user

            # Parse profile picture
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            
            # Save instance
            profile.save()
            registered = True
        
        # Form was invalid
        else:
            print(user_form.errors, profile_form.errors)

    # Not HTTP POST, render the empty forms for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})

"""
    @brief Shows login view for users
    @param request
    @return Redirect if the user logs in successfully,
            Render of the login form if the request is GET
            HttpResponse if login fails.
"""
def user_login(request):
    # Pull details from POST login
    login_form = LoginForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # If login details correct
        if user:
            # Account is active
            if user.is_active:
                login(request, user)
                return redirect(reverse('spuni:index'))
            else:
                return HttpResponse("Sorry, your spuni account has been deactivated! Contact us regarding reactivation of your account.")
        # Incorrect login details
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details.")
    # Display get login form
    else:
        return render(request, 'login.html',
                        context = {"login_form": login_form})

"""
    @brief Display form to request to add a song
    @param request
    @return render
"""
@login_required
def add_song(request):
    form = SongForm()
    
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            """
            NOTE:
                Here I think that we'd make commit=False
                And call some sort of function on the backend
                to fill out the other details of the model
            """
            try:
                song = form.save(commit=True)
                return redirect(reverse('spuni:show_song',
                                kwargs={'song_name_slug':song.slug}))
            except:
                return redirect('/')
        else:
            print(form.errors)
    return render(request, 'add_song.html', {'form':form})

"""
    @brief Shows the search view for a given query
           Search view is populated by the spotify API
    @param query: The query e.g. song name to search
    @return The render
"""
def search_song(request, query):
    print("---------------")
    print(query)
    print("---------------")
    context_dict = {'songs': search(query)}
    # Try to check if any of these models already exist
    for song in context_dict['songs']:
        try:
            # If the song already exists, update the dict to reflect the model
            # instance instead of the spotify result.
            s = Song.objects.get(slug=context_dict['songs'][song]["slug"],
                                    name=context_dict['songs'][song]["name"],
                                    artist=context_dict['songs'][song]["artist_name"])
            context_dict['songs'][song].update({'name':s.name,
                                                'artist_name':s.artist,
                                                'album_art':s.albumArt,
                                                'slug':s.slug,
                                                'slug':s.upvotes})
        except ObjectDoesNotExist:
            pass
        
    if request.user.is_authenticated:
        username = request.user.username
        context_dict["username"] = username
    return render(request, 'search.html', context_dict)

"""
    @brief Shows the given user's profile
    @param request Request object
    @param username Username of the user's profile to show
"""    
@login_required
def show_profile(request, username):
    context_dict = {}
    try:
        u = UserProfile.objects.get(user=User.objects.get(username=username))
        context_dict['user'] = u
        context_dict['username'] = username
        context_dict['songs'] = u.upvotedSongs.all()
    except (User.DoesNotExist, UserProfile.DoesNotExist) as e:
        context_dict['user'] = None
        context_dict['username'] = None
        context_dict['songs'] = u.upvotedSongs.all()

    print(request.user.is_authenticated)
    return render(request, 'profile.html', context=context_dict) 

"""
    @brief Given a username and songname, either creates
           a new relationship or leaves the relationship
           unchanged. Also increments song's upvote value
    @param request: A dictionary in the format: 
                    {"username":, "slug":, "name":, "albumArt":, "artist":}
                    "name", "albumArt", and "artist", may be ommitted if it is
                    known that the model instance already exists (e.g. on the index page),
                    however these must be included in any page which may include song instances
                    that do not already exist in the database (e.g. on the search page).
                    OR a request object
"""
def upvote(request):
    # We only accept GET requests from authenticated users.
    # We also bypass authentication if the process is called from the population script.
    if (type(request) != dict):
        if (request.method != "GET"):
            print("Not a GET.")
            return render(request, 'index.html')

        if (not request.user.is_authenticated):
            print("Not authenticated.")
            return render(request, 'index.html')

    # We have the dict versus normal because the population script also uses the upvote
    # function. Meanwhile the requests don't use dict.
    if (type(request) == dict):
        username = request["username"]

        # Checks if the slug has been supplied in the dict
        if ("slug" in request.keys()):
            slug = request["slug"]
        else:
            slug = None

        # If the artist and albumArt was also passed in
        # this is indicative that we need all the information to create
        # a new song instance.
        if (("artist" in request.keys()) and ("albumArt" in request.keys())
                and ("name" in request.keys())):
            name = request["name"]
            artist = request["artist"]
            albumArt = request["albumArt"]
        else:
            name = None
            artist = None
            albumArt = None
    else:
        username = request.user.username
        slug = request.GET.get('slug', None)
        name = request.GET.get('name', None)
        artist = request.GET.get('artist', None)
        albumArt = request.GET.get('albumArt', None)

    # Get objects from database for the given parameters.
    user_profile = UserProfile.objects.get(user=User.objects.get(username=username))
    
    # Check if the song actually exists first
    try:
        song = Song.objects.get(slug=slug)
    # If it doesn't exist, create the song
    except ObjectDoesNotExist:
        # requires that all details must have been passed in the
        # request (either dictionary or request object)
        if ((artist != None) and (albumArt != None) and (name != None)):
            song = Song.objects.create(name=name, albumArt=albumArt,
                                        upvotes=0, artist=artist)
        # A new song instance was unable to be created
        else:
            return render(request, 'index.html')

    # Check if the user has already upvoted this song.
    try:
        user_profile.upvotedSongs.get(slug=slug)
        print("Already done.")
    except ObjectDoesNotExist:
        # If not, then we upvote the song.
        user_profile.upvotedSongs.add(song)
        print(song.upvotes)
        song.upvotes += 1
        print("UPVOTED")
        print(song.upvotes)
        song.save()
    
    if (type(request) == dict):
        return
    else:
        return render(request, 'index.html')

"""
    @brief Given a username and songname, if a relationship
           exists, removes it and decrements the song.
    @param request: A dictionary in the format of {"username":, "songname":} 
                    OR a request object 
"""
def downvote(request):
    # We only accept GET requests from authenticated users.
    if (type(request) != dict):
        if (request.method != "GET"):
            print("Not a GET.")
            return render(request, 'index.html')

        if (not request.user.is_authenticated):
            print("Not authenticated.")
            return render(request, 'index.html')

    # We have the dict versus normal because the population script also uses the upvote
    # function. Meanwhile the requests don't use dict.
    if (type(request) == dict):
        username = request["username"]
        songname = request["songname"]
    else:
        username = request.user.username
        songname = request.GET.get('songname', None)

    # Get objects from database for the given parameters.
    user_profile = UserProfile.objects.get(user=User.objects.get(username=username))

    try:
        song = Song.objects.get(slug=songname)
        # Check if the user has already downvoted this song.
        try:
            user_profile.upvotedSongs.get(slug=songname)
            user_profile.upvotedSongs.remove(song)
            print(song.upvotes)
            song.upvotes -= 1
            print("DOWNVOTED")
            print(song.upvotes)
            song.save()
        except ObjectDoesNotExist:
            pass
    # The song to be downvoted doesn't exist in the model
    # This choice does not allow for negative downvotes
    except ObjectDoesNotExist:
        return render(request, 'index.html')
    
    if (type(request) == dict):
        return
    else:
        return render(request, 'index.html')