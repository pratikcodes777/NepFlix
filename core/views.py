from django.shortcuts import render
from videos.models import Video, TVShow, Movie, WatchProgress
# Create your views here.

def home(request):
    category = request.GET.get('category', 'all')
    
    if request.user.is_authenticated:
        recently_watched = WatchProgress.objects.filter(
            user=request.user,
            current_position__gte=10  
        ).order_by('-last_watched')[:10]  
    else:
        recently_watched = None

    # Filter videos based on category
    if category == 'movies':
        videos = Movie.objects.all()
    elif category == 'shows':
        videos = TVShow.objects.all()
    else:
        videos = Video.objects.all()

    context = {
        'videos': videos,
        'selected_category': category,
        'recently_watched': recently_watched
    }

    if request.headers.get('HX-Request'):
        return render(request, 'videos/video_list_partial.html', {'videos': videos})

    return render(request, 'home.html', context)



def search_videos(request):
    query = request.GET.get('q')
    if query:
        results = Video.objects.filter(title__icontains=query)
    else:
        results = Video.objects.none()
    context = {
        'videos': results,
        'query': query
    }
    return render(request, 'videos/search_results.html', context)



