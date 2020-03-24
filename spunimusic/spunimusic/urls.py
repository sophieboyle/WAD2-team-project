from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from spuni import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('social/', include('social_django.urls')),
    path('', include('django.contrib.auth.urls')),
    # path('', include('userprofile.urls')),
    path('auth', include('django.contrib.auth.urls')),
    path('spuni/', include('spuni.urls')),

    url(r'^upvote/$', views.upvote, name='upvote'),
    url(r'^downvote/$', views.downvote, name='downvote')
]
