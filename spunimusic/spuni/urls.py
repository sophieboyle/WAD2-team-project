from django.urls import path
from spuni import views

app_name = 'song'

urlpatterns = [
    path('<int:song_id>/', views.show_song, name='show_song'),
]