from django.contrib.auth.models import User
from spuni.models import UserProfile, Song
from django import forms

"""
    User form to fill in user model fields
    to create a new user.
"""
class UserForm(forms.ModelForm):
    # Explicit definition conceals password
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

"""
    Login form presenting a username and password
    field, allowing user's to login.
"""
class LoginForm(forms.ModelForm):
    # Explicit definition conceals password
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

"""
    UserProfile form which presents the photo
    field, allowing a user to provide a url to
    a photo to add to their UserProfile instance.
"""
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)

"""
    Song form, allowing users to fill in a
    song name and an artist name. (Unused)
"""
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('name', 'artist',)

"""
    EditUserProfile form, allowing a user
    to change the photo url of their UserProfile
    instance.
"""
class EditUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        user = kwargs.get('instance')
        if user:
            self.fields["photo"].initial = user.photo
    
    class Meta:
        model = UserProfile
        fields = ('photo',)
        # exclude = ('user',)