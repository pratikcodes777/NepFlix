from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Playlist, PlaylistItem
from .forms import PlaylistForm, PlaylistItemForm, PlaylistSelectionForm
from videos.models import Video


def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST ,  request.FILES )
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, 'Playlist created successfully!')
            return redirect('playlist_list')
    else:
        form = PlaylistForm()

    return render(request, 'playlists/create_playlist.html', {'form': form})


def update_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Playlist updated successfully!')
            return redirect('playlist_list')  
    else:
        form = PlaylistForm(instance=playlist)

    context = {
        'form': form,
        'playlist': playlist
    }

    return render(request, 'playlists/update_playlist.html', context)


def add_video_to_playlist(request, video_slug):
    video = get_object_or_404(Video, slug=video_slug)

    if request.method == 'POST':
        form = PlaylistSelectionForm(request.user, request.POST)
        if form.is_valid():
            playlist = form.cleaned_data['playlist']
            PlaylistItem.objects.get_or_create(playlist=playlist, video=video)
            messages.success(request, f'Video "{video.title}" added to playlist "{playlist.title}".')
            return redirect('playlist_list')
    else:
        form = PlaylistSelectionForm(user=request.user)

    return render(request, 'playlists/add_video_to_playlist.html', {'form': form, 'video': video})



def playlist_list(request):
    playlists = request.user.playlists.all()
    return render(request, 'playlists/playlist_list.html', {'playlists': playlists})



def public_playlist(request):
    playlists = Playlist.objects.filter(type='Public')
    print(playlists)
    return render(request, 'playlists/public_list.html', {'playlists': playlists})



def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    items = playlist.items.all()
    return render(request, 'playlists/playlist_detail.html', {'playlist': playlist, 'items': items})



def remove_video_from_playlist(request, playlist_id, video_slug):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    video = get_object_or_404(Video, slug=video_slug)

    item = PlaylistItem.objects.filter(playlist=playlist, video=video).first()
    if item:
        item.delete()
        messages.success(request, f'Video "{video.title}" removed from playlist "{playlist.title}".')
    else:
        messages.error(request, 'Video not found in playlist.')

    return redirect('playlist_detail', playlist_id=playlist.id)



def delete_playlist(request, id):
    playlist = get_object_or_404(Playlist, id=id)
    
    if request.method == 'POST':
        playlist.delete()
        messages.success(request , 'Playlist deleted successfully.')
        return redirect('playlist_list') 

    return render(request, 'playlists/confirm_delete.html', {'playlist': playlist})