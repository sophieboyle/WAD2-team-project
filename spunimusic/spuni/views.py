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
"""
def index(request):
    song_list = Song.objects.order_by('-upvotes')
    context_dict = {'songs': song_list}
    print(context_dict)
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        username = request.user.username
        context_dict["username"] = username
        
        return render(request, 'index.html', context_dict)
    else:
        return render(request, 'index.html', context_dict)
    

"""
    @brief Logout view
    @param request
"""
def logout(request):
    auth_logout(request)
    return index(request)


"""
    @brief Shows the registration forms for new users to register
    @param request
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
    @brief Shows the given user's profile
    @param request
    @param username
"""
def search_song(request, query):
    print("---------------")
    print(query)
    print("---------------")
    context_dict = {'songs': search(query)}
    if request.user.is_authenticated:
        username = request.user.username
        context_dict["username"] = username
    return render(request, 'search.html', context_dict)
    
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
    return render(request, 'profile.html', context=context_dict) 
