from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls')),
    path('', include('django.contrib.auth.urls')),
    # path('', include('userprofile.urls')),
    path('auth', include('django.contrib.auth.urls')),
    path('spuni/', include('spuni.urls')),
]
