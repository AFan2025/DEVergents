from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse

from MoodMusic.models import UserSongMoods, Song
import random

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

    return HttpResponse(response_text)


def song_search(request):
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(title__icontains=query)
    else:
        songs = Song.objects.none()
    return render(request, 'search_results.html', {'songs': songs})