from django.urls import path
from spuni import views

app_name = 'song'

urlpatterns = [
    path('<slug:song_name_slug>/', views.show_song, name='show_song'),
]