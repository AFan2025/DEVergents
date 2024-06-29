"""
URL configuration for Tiktok project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MoodMusic import views
from django.contrib.auth import views as auth_views
from MoodMusic.views import ProfileView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('about.html', views.about, name='about'), 
    path('create_user_song_mood/', views.create_user_song_mood, name='create_user_song_mood'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('find_songs/', views.find_songs, name='find_songs'),
    path('add_song/', views.add_song, name='add_song'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path("search/", views.song_search),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tiktok/login/', views.tiktok_login, name='tiktok_login'),
    path('tiktok/callback/', views.tiktok_callback, name='tiktok_callback'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
]
