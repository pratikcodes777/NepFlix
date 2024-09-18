from django import forms
from .models import Playlist, PlaylistItem

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'description' , 'image_file' , 'type']

class PlaylistItemForm(forms.ModelForm):
    class Meta:
        model = PlaylistItem
        fields = []


class PlaylistSelectionForm(forms.Form):
    playlist = forms.ModelChoiceField(queryset=None, label="Select Playlist", empty_label="Choose Playlist")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['playlist'].queryset = user.playlists.all()