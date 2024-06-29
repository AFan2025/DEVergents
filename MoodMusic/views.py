from django.shortcuts import redirect, render

# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from MoodMusic.models import UserSongMoods, Song, Friendship
import random
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json
import requests
from django.conf import settings

def about(request):
    return render(request, 'about.html')

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
    access_token = request.session.get('spotify_access_token')
    songs = Song.objects.all()
    moods = UserSongMoods.objects.all()
    if not songs:
        return render(request, 'find-songs.html', {'message': 'No songs available'})
    random_song = random.choice(songs)
    mood_count = UserSongMoods.objects.count()
    random_mood1_index = random.randint(0, mood_count - 1)
    random_mood2_index = random.randint(0, mood_count - 1)
    random_mood1 = UserSongMoods.objects.all()[random_mood1_index].moods
    random_mood2 = UserSongMoods.objects.all()[random_mood2_index].moods
    return render(request, 'find-songs.html', {
        'song': random_song,
        'mood1': random_mood1,
        'mood2': random_mood2,
        'access_token': access_token,
    })

@login_required
def add_song(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        mood = request.POST.get('mood')
        try:
            song = Song.objects.get(title=title, artist=artist)  # Use get() to fetch a single song
        except Song.DoesNotExist:
            return render(request, 'add-song.html', {'error': 'Song not found'})

        # Create or update the mood associated with the song for the current user
        UserSongMoods.objects.update_or_create(
            user=request.user,
            song=song,
            defaults={'moods': mood}
        )
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
    
    # Get the search query if it exists
    query = request.GET.get('q')
    
    if query:
        # Filter UserSongMoods objects based on the search query
        user_song_moods = UserSongMoods.objects.filter((Q(user=user) & Q(song__title__icontains=query)) | (Q(user=user) & Q(moods__icontains=query)) | (Q(user=user) & Q(song__artist__icontains=query)))
    else:
        # If no search query, get all UserSongMoods for this user
        user_song_moods = UserSongMoods.objects.filter(user=user)
    friends = Friendship.objects.filter(Q(friend1=user) | Q(friend2=user))
    
    context = {
        'username': user.username,
        'songs': user_song_moods,
        'query': query,
        'friends': friends,
    }
    
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

def tiktok_login(request):
    # Redirect to TikTok authorization URL
    auth_url = f"https://www.tiktok.com/auth/authorize/?client_key={settings.TIKTOK_CLIENT_KEY}&scope=user.info.basic,video.list&response_type=code&redirect_uri={settings.TIKTOK_REDIRECT_URI}"
    return redirect(auth_url)

def tiktok_callback(request):
    # Handle TikTok callback and get access token
    code = request.GET.get('code')
    token_url = 'https://open.tiktokapis.com/oauth/access_token/'
    data = {
        'client_key': settings.TIKTOK_CLIENT_KEY,
        'client_secret': settings.TIKTOK_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.TIKTOK_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data)
    response_data = response.json()
    
    # Save the access token and open_id in session
    request.session['tiktok_access_token'] = response_data['data']['access_token']
    request.session['tiktok_open_id'] = response_data['data']['open_id']
    
    return redirect('add_song')

def fetch_tiktok_videos(request):
    access_token = request.session.get('tiktok_access_token')
    if not access_token:
        return redirect('tiktok_login')  # Redirect to TikTok login if not authenticated
    
    video_list_url = 'https://open.tiktokapis.com/v2/video/list/?fields=id,title,video_description,duration,cover_image_url,embed_link'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(video_list_url, headers=headers, json={'max_count': 20})
    response_data = response.json()
    
    return render(request, 'add_song.html', {'videos': response_data['data']['videos']})

def spotify_login(request):
    client_id = '50dc5ab5c541453c8d97147d2737bdb9'
    redirect_uri = 'http://127.0.0.1:8000/spotify/callback/'
    scope = 'user-read-playback-state user-modify-playback-state streaming'
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}'
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    access_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')
    request.session['spotify_access_token'] = access_token
    request.session['spotify_refresh_token'] = refresh_token
    return redirect('find_songs')