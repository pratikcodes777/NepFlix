from django.contrib import admin
from .models import Playlist, PlaylistItem
# Register your models here.

admin.site.register(Playlist)
admin.site.register(PlaylistItem)

