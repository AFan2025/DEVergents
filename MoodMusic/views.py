from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from MoodMusic.models import UserSongMoods, Song
import random
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json

@login_required
def create_user_song_mood(request):
    if request.method == 'POST':
        print("POST request received")  # Debugging statement
        data = json.loads(request.body)
        song_id = data.get('song_id')
        mood = data.get('mood')
        user = request.user

        print(f"User: {user}, Song ID: {song_id}, Mood: {mood}")  # Debugging statement

        song = get_object_or_404(Song, id=song_id)
        UserSongMoods.objects.create(user=user, song=song, moods=mood)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

def home(request):
    return render(request, 'index.html')

def find_songs(request):
    # Fetch all songs from the database
    songs = Song.objects.all()
    moods = UserSongMoods.objects.all()
    if not songs:
        # If there are no songs, handle the case gracefully
        return render(request, 'find-songs.html', {'message': 'No songs available'})
    
    # Select a random song
    random_song = random.choice(songs)
    mood_count = UserSongMoods.objects.count()
    random_mood1_index = random.randint(0, mood_count - 1)
    random_mood2_index = random.randint(0, mood_count - 1)
    random_mood1 = UserSongMoods.objects.all()[random_mood1_index].moods
    random_mood2 = UserSongMoods.objects.all()[random_mood2_index].moods
    
    # Render the template with the random song
    return render(request, 'find-songs.html', {'song': random_song, 'mood1': random_mood1, 'mood2': random_mood2})

def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        if title and artist:
            Song.objects.create(title=title, artist=artist)
            return redirect('home')
    return render(request, 'add-song.html')

def test(request):
    try:
        p = UserSongMoods.objects.get(moods='Happy')
    except UserSongMoods.DoesNotExist:
        raise Http404("Usersongmood does not exist")
    return HttpResponse(p.user.username)

def get_swipe_info(request):
    try:
        song_count = Song.objects.count()
        mood_count = UserSongMoods.objects.count()
        
        if song_count == 0 or mood_count == 0:
            raise Http404("No songs or moods available")
        
        random_song_index = random.randint(0, song_count - 1)
        random_song = Song.objects.all()[random_song_index]

        random_mood1_index = random.randint(0, mood_count - 1)
        random_mood2_index = random.randint(0, mood_count - 1)
        random_mood1 = UserSongMoods.objects.all()[random_mood1_index].moods
        random_mood2 = UserSongMoods.objects.all()[random_mood2_index].moods

        song_info = f'{random_song.title} by {random_song.artist}'
        response_text = f'{song_info}-- Do you think it is more {random_mood1} or {random_mood2}?'
        
    except UserSongMoods.DoesNotExist:
        raise Http404("Usersongmood does not exist")

    data = {
        'song_info': song_info,
        'mood_options': [random_mood1, random_mood2],
        'message': response_text
    }

    # Return the data as JSON
    return JsonResponse(data)

def profile(request, username):
    # Get the user object or return a 404 if the user does not exist
    user = get_object_or_404(User, username=username)
    
    # Filter UserSongMoods objects for this user
    user_song_moods = UserSongMoods.objects.filter(user=user)
    
    # Prepare the data to be returned
    context = {
        'username': user.username,
        'user_song_moods': user_song_moods
    }
    
    # Render the profile template with the context data
    return render(request, 'profile.html', context)

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request, username, *args, **kwargs):
        # Get the user object or return a 404 if the user does not exist
        user = get_object_or_404(User, username=username)

        # Filter UserSongMoods objects for this user
        user_song_moods = UserSongMoods.objects.filter(user=user)

        # Prepare the data to be returned
        context = {
            'username': user.username,
            'user_song_moods': user_song_moods
        }

        # Render the profile template with the context data
        return render(request, 'profile.html', context)

def song_search(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    else:
        songs = Song.objects.none()
    data = {
        'songs': [
            {
                'title': song.title,
                'artist': song.artist,
            }
            for song in songs
        ]
    }
    # Return the data as JSON
    return JsonResponse(data)