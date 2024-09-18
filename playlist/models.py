from django.db import models
from users.models import CustomUser
from videos.models import Video


class Playlist(models.Model):
    playlist_choice = {
        ('Public' , 'Public'),
        ('Private' , 'Private'),
    }
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    image_file = models.ImageField(upload_to='playlist_image/')
    type = models.CharField(max_length=20 , choices=playlist_choice , null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'video')

    def __str__(self):
        return f'{self.video.title} in {self.playlist.title}'