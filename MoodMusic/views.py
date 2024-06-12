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
        a = random.randint(0,1)
        b = random.randint(0,1)
        c = random.randint(0,1)
        random_song = (f'{Song.objects.all()[a].title} by {Song.objects.all()[a].artist}')
        random_mood1 = (UserSongMoods.objects.all()[b].moods)
        random_mood2 = (UserSongMoods.objects.all()[c].moods)
    except UserSongMoods.DoesNotExist:
        raise Http404("Usersongmood does not exist")
    return HttpResponse(f'{random_song}-- Do you think it is more {random_mood1} or {random_mood2}?')