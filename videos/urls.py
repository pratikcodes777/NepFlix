from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-movies' , views.all_movies , name='movies'),
    path('all-shows' , views.all_shows , name='shows'),
    path('recent-videos' , views.recent_videos , name='recent-videos'),
    path('add-video' , views.add_video , name='add-video'),
    path('video_details/<slug:slug>' , views.video_details , name='video_details'),
    path('videos/update/<slug:slug>/', views.update_video, name='update_video'),
    path('videos/<slug:slug>/delete/', views.delete_video, name='delete_video'),
    path('video/<slug:slug>/increment_watch_count/', views.increment_watch_count, name='increment_watch_count'),
    path('save_progress/<int:video_id>/', views.save_progress, name='save_progress'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
