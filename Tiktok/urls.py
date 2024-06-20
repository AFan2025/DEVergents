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

urlpatterns = [
    path('create_user_song_mood/', views.create_user_song_mood, name='create_user_song_mood'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('find_songs/', views.find_songs, name='find_songs'),
    path('add_song/', views.add_song, name='add_song'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('testpath/', views.test),
    path('swipe/', views.get_swipe_info),
    path("search/", views.song_search),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
