from django.shortcuts import render
from django.contrib.auth import logout as auth_logout


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        return render(request, 'userprofile/index.html', {'username':username})
    else:
        return render(request, 'userprofile/index.html')
    

def logout(request):
    auth_logout(request)
    return render('userprofile/index.html')