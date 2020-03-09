from django.contrib.auth.models import User
from spuni.models import UserProfile
from django import forms


class UserForm(forms.ModelForm):
    # Explicit definition conceals password
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo',)