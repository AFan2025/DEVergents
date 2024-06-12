from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse

from MoodMusic.models import UserSongMoods, Song


def test(request):
    try:
        p = UserSongMoods.objects.get(moods='Happy')
    except UserSongMoods.DoesNotExist:
        raise Http404("Usersongmood does not exist")
    return HttpResponse(p.user.username)