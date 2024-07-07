from django.shortcuts import redirect, render

# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from MoodMusic.models import UserSongMoods, Song, Friendship, NumMoodsSong
import random
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json
import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib import messages

COLUMN_MAP = {'Happy': 'numHappy',
 'Sad': 'numSad',
 'Exciting': 'numExciting',
 'Calming': 'numCalming',
 'Angering': 'numAngering',
 'Relaxing': 'numRelaxing',
 'Motivating': 'numMotivating',
 'Melancholic': 'numMelancholic',
 'Anxious': 'numAnxious',
 'Joyful': 'numJoyful',
 'Contenting': 'numContenting',
 'Nostalgic': 'numNostalgic',
 'Peaceful': 'numPeaceful',
 'Energizing': 'numEnergizing',
 'Boring': 'numBoring',
 'Hopeful': 'numHopeful',
 'Lonely': 'numLonely',
 'Frustrating': 'numFrustrating',
 'Curious': 'numCurious',
 'Confident': 'numConfident',
 'Guilty': 'numGuilty',
 'Surprising': 'numSurprising',
 'Proud': 'numProud',
 'Scaring': 'numScaring',
 'Shy': 'numShy',
 'Grateful': 'numGrateful',
 'Disappointing': 'numDisappointing',
 'Loving': 'numLoving',
 'Worrying': 'numWorrying',
 'Indifferent': 'numIndifferent',
 'Elating': 'numElating',
 'Sorrowful': 'numSorrowful',
 'Amusing': 'numAmusing',
 'Apathetic': 'numApathetic',
 'Enthusiastic': 'numEnthusiastic',
 'Jealous': 'numJealous',
 'Ashamed': 'numAshamed',
 'Relieving': 'numRelieving',
 'Serene': 'numSerene',
 'Playful': 'numPlayful',
 'Restless': 'numRestless',
 'Tiring': 'numTiring',
 'Focusing': 'numFocusing',
 'Determining': 'numDetermining',
 'Sympathetic': 'numSympathetic',
 'Optimistic': 'numOptimistic',
 'Pessimistic': 'numPessimistic',
 'Bewildering': 'numBewildering',
 'Overwhelming': 'numOverwhelming',
 'Inspiring': 'numInspiring'}

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

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
    while random_mood1==random_mood2:
        random_mood2_index = random.randint(0, mood_count - 1)
        random_mood2 = UserSongMoods.objects.all()[random_mood2_index].moods
    return render(request, 'find-songs.html', {
        'song': random_song,
        'mood1': random_mood1,
        'mood2': random_mood2,
        'access_token': access_token,
    })

# @login_required
# def add_song(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         artist = request.POST.get('artist')
#         mood = request.POST.get('mood')
#         try:
#             song = Song.objects.get(title=title, artist=artist)  # Use get() to fetch a single song
#         except Song.DoesNotExist:
#             return render(request, 'add-song.html', {'error': 'Song not found'})

#         # Create or update the mood associated with the song for the current user
#         UserSongMoods.objects.update_or_create(
#             user=request.user,
#             song=song,
#             defaults={'moods': mood}
#         )
#         return redirect('home')
    
#     return render(request, 'add-song.html')





## General flow:
    ##add_song2 -> (rate_song -> rate-song.html -> increment_song) x15 -> home

def rate_song(request, nummoods_id):
    access_token = request.session.get('spotify_access_token')
    numsong_obj = NumMoodsSong.objects.get(id = nummoods_id)
    song_obj = getattr(numsong_obj, "song")

    mood1, colid1 = random.choice(list(COLUMN_MAP.items()))
    mood2, colid2 = random.choice(list(COLUMN_MAP.items()))
    while mood1 == mood2:
        mood2, colid2 = random.choice(list(COLUMN_MAP.items()))
    return render(request, 'find-songs.html', {
        'numsong_obj': numsong_obj,
        'song': song_obj,
        'mood1': mood1,
        'mood2': mood2,
        'access_token': access_token,
    })



    if request.method == 'POST':
        data = request.POST
        # song = data.get("song")
        # user = data.get("user")

        # #find the user song pairing
        # try:
        #     nummoods = NumMoodsSong.objects.get(song=song, user=user) 
        # except NumMoodsSong.DoesNotExist:
        #     return render(request, "rate_song.html", {'error': 'Song not found'})

        ## Dependent on how it is returned from the html file
        mood = data.get("mood")

        ##increments the mood file by 1
        response = increment_mood(nummoods_id, mood)

        if json.loads(response.content).get("rateLimit") > 15:
            redirect('home')
        else:
            return render(request, "rate_song.html")


    #     nummoodsong.count += 1
    #     nummoodsong.save()
    #     return JsonResponse({'status': 'success', 'count': counter.count})


    # nummoodsong = get_object_or_404(NumMoodsSong, id=nummoods_id)
    
    
    # return render(request, "rate_song.html", {'counter': response.content["new_value"]})
    return render(request, "rate_song.html")

def increment_mood(request):
    if request.method == 'POST':
        data = request.POST
        nummoods_id = data.get("nummoods_id")
        mood = data.get("mood")

     # Get the DataRecord instance
    nummoodsong = get_object_or_404(NumMoodsSong, id=nummoods_id)

    # Get the column name from the mapping dictionary
    column_name = COLUMN_MAP.get(mood)

    curval = getattr(nummoodsong, column_name)
    curratelim = getattr(nummoodsong, "rateLimit")

    if curratelim < 14:
        setattr(nummoodsong, column_name, curval + 1)
        setattr(nummoodsong, "rateLimit", curratelim + 1)
        nummoodsong.save()
        return JsonResponse({'status': 'success',
                            'mood': column_name,
                            'new_value': curval + 1, 
                            "rateLimit": curratelim + 1})
    # if curratelim == 14:
    #     setattr(nummoodsong, column_name, curval + 1)
    #     setattr(nummoodsong, "rateLimit", curratelim + 1)
    #     nummoodsong.save()
    #     return JsonResponse({'status': 'final', 'new_value': curval + 1})
    elif curratelim == 14:
        setattr(nummoodsong, column_name, curval + 1)
        setattr(nummoodsong, "rateLimit", curratelim + 1)
        nummoodsong.save()
        return JsonResponse({'status': 'limit',
                            'mood': column_name,
                            'new_value': curval + 1, 
                            "rateLimit": curratelim + 1})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid action'}, status=400)


    # if request.method == 'POST':
    #     # data = request.POST
    #     # action = data.get('action')
    #     # new_value = data.get('new_value')

    if column_name and hasattr(nummoodsong, column_name):
        setattr(record, column_name, int(new_value))
        nummoodsong.save()
        return JsonResponse({'status': 'success', 'new_value': new_value})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid action'}, status=400)


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
        new = NumMoodsSong.objects.get_or_create(
            user = request.user,
            song = song,
            defaults = {element: 0 for element in COLUMN_MAP.values()}
        )
        return redirect('rate-song', nummoods_id = new.id)
    
    return render(request, 'add-song.html')

























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
    num_songs_rated = user_song_moods.count()
    num_moods = user_song_moods.values('moods').distinct().count()
    num_friends = Friendship.objects.filter(Q(friend1=user) | Q(friend2=user)).count()
    
    context = {
        'username': user.username,
        'songs': user_song_moods,
        'query': query,
        'friends': friends,
        'num_songs_rated': num_songs_rated,
        'num_moods': num_moods,
        'num_friends': num_friends,
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
    
@login_required
def add_friend(request):
    if request.method == "POST":
        username = request.POST.get('username')

        if username:
            if len(User.objects.filter(username=username)) == 0:
                return redirect('profile', username=request.user.username)
            friend = get_object_or_404(User, username=username)
            switch = Friendship.objects.filter(Q(friend1=friend, friend2=request.user) | Q(friend1=request.user, friend2=friend))
            if switch.count() == 0 and friend != request.user:
                Friendship.objects.get_or_create(friend1=request.user, friend2=friend)
                return redirect('profile', username=request.user.username)
            else:
                return redirect('profile', username=request.user.username)
            
    return redirect('profile', username=request.user.username)

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