from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.index, name='index'),
]