from django.contrib.auth.models import User
from spuni.models import UserProfile, Song
from django import forms


class UserForm(forms.ModelForm):
    # Explicit definition conceals password
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class LoginForm(forms.ModelForm):
    # Explicit definition conceals password
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('name', 'artist',)
    
class EditUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        self.fields["photo"].initial = user.photo
    
    class Meta:
        model = UserProfile