from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from MoodMusic.models import Song, UserSongMoods

class Command(BaseCommand):
    help = 'Add predefined moods to the database'

    def handle(self, *args, **kwargs):
        moods = [
            "Happy", "Sad", "Exciting", "Calming", "Angering", "Relaxing", "Motivating", "Melancholic",
            "Anxious", "Joyful", "Contenting", "Nostalgic", "Peaceful", "Energizing", "Boring", "Hopeful",
            "Lonely", "Frustrating", "Curious", "Confident", "Guilty", "Surprising", "Proud", "Scaring",
            "Shy", "Grateful", "Disappointing", "Loving", "Worrying", "Indifferent", "Elating", "Sorrowful",
            "Amusing", "Apathetic", "Enthusiastic", "Jealous", "Ashamed", "Relieving", "Serene", "Playful",
            "Restless", "Tiring", "Focusing", "Determining", "Sympathetic", "Optimistic", "Pessimistic", "Bewildering", "Overwhelming", "Inspiring"
        ]



        user = User.objects.first() 
        song = Song.objects.first()

        if not user or not song:
            self.stdout.write(self.style.ERROR('User or Song not found. Please ensure both exist.'))
            return

        for mood in moods:
            UserSongMoods.objects.get_or_create(user=user, song=song, moods=mood)

        self.stdout.write(self.style.SUCCESS('Successfully added predefined moods.'))
