from django.urls import path
from spuni import views

app_name = 'spuni'

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.index, name='index'),
    path('song/<slug:song_name_slug>/', views.show_song, name='show_song'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login')
]
