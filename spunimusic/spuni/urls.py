from django.urls import path
from spuni import views

app_name = 'spuni'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_song, name='add_song'),
    path('song/<slug:song_name_slug>/', views.show_song, name='show_song'),
    path('search/<query>/', views.search_song, name='search_song'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<slug:username>/', views.show_profile, name='show_profile'),
    path('edit/', views.edit_profile, name='edit_profile')
]
