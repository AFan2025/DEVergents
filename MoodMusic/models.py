from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
        unique_together = ('user', 'song', 'moods')

class Friendship(models.Model):
    friend1 = models.ForeignKey(User, on_delete = models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name='friend2')

class NumMoodsSong(models.Model):
    #Ties it to the user and the song
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    song = models.ForeignKey(Song, on_delete = models.CASCADE)

    #has an integer value for every Mood we have so far
    numHappy = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numSad = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numExciting = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numCalming = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])
    numAngering = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numRelaxing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numMotivating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numMelancholic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numAnxious = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numJoyful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numContenting = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numNostalgic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numPeaceful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numEnergizing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numBoring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numHopeful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numLonely = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numFrustrating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numCurious = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numConfident = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)])  
    numGuilty = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numSurprising = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numProud = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numScaring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numShy = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numGrateful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numDisappointing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numLoving = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numWorrying = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numIndifferent = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numElating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numSorrowful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numAmusing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numApathetic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numEnthusiastic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numJealous = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numAshamed = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numRelieving = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numSerene = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numPlayful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numRestless = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numTiring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numFocusing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numDetermining = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numSympathetic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numOptimistic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numPessimistic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numBewildering = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numOverwhelming = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 
    numInspiring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(0)]) 

def separate_moods(s):
    return s.split(',')