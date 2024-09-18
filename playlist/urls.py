from django.urls import path
from . import views

urlpatterns = [
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<slug:video_slug>/add-to-playlist/', views.add_video_to_playlist, name='add_video_to_playlist'),
    path('playlist/<int:playlist_id>/remove/<slug:video_slug>/', views.remove_video_from_playlist, name='remove_video_from_playlist'),
    path('playlist/<int:id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('update/<int:playlist_id>/', views.update_playlist, name='update_playlist'),
    path('public-playlist/' , views.public_playlist , name='public-playlist')
]
