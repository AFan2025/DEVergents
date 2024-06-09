from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length = 100)
    artist = models.CharField(max_length = 100)
    
    def __str__(self):
        return f"{self.title} by {self.artist}"
    
class UserSongMoods(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    song = models.ForeignKey(Song, on_delete = models.CASCADE)
    moods = models.TextField(help_text = "Enter moods separated by commas")
    
    def __str__(self):
        return f"{self.user.username} - {self.song}"
    
    class Meta:
        unique_together = ('user', 'song')
    