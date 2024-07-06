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
    numHappy = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numSad = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numExciting = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numCalming = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])
    numAngering = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numRelaxing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numMotivating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numMelancholic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numAnxious = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numJoyful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numContenting = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numNostalgic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numPeaceful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numEnergizing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numBoring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numHopeful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numLonely = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numFrustrating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numCurious = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numConfident = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)])  
    numGuilty = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numSurprising = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numProud = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numScaring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numShy = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numGrateful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numDisappointing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numLoving = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numWorrying = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numIndifferent = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numElating = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numSorrowful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numAmusing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numApathetic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numEnthusiastic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numJealous = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numAshamed = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numRelieving = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numSerene = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numPlayful = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numRestless = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numTiring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numFocusing = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numDetermining = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numSympathetic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numOptimistic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numPessimistic = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numBewildering = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numOverwhelming = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 
    numInspiring = models.IntegerField(default=0, validators=[MaxValueValidator(3),MinValueValidator(1)]) 

def separate_moods(s):
    return s.split(',')