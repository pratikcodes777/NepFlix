from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import TVShow, Movie, Category, Video, WatchProgress
from django.contrib import messages
from datetime import timedelta
from .forms import ReviewForm
from django.utils.text import slugify
import json

# Create your views here.

def all_movies(request):
    # returns only the videos whose categories is movies 
    movies = Movie.objects.all()
    context = {
        'movies':movies
    }
    return render(request , 'videos/all_movies.html' , context)


def all_shows(request):
    # returns only the videos whose categories is shows 
    shows = TVShow.objects.all()
    context = {
        'shows':shows
    }
    return render(request , 'videos/all_shows.html', context)




def video_details(request, slug):
    video = get_object_or_404(Video, slug=slug)
    reviews = video.reviews.all()
    user_review = video.user_review(request.user)
    average_rating = video.average_rating()
    full_stars = int(average_rating)
    half_stars = 1 if average_rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars

    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = ReviewForm(request.POST, instance=user_review) if user_review else ReviewForm(request.POST)
            
            if form.is_valid():
                review = form.save(commit=False)
                review.video = video
                review.user = request.user
                review.save()
                
                review_html = render_to_string('videos/review_item.html', {'review': review}, request=request)
                return JsonResponse({'status': 'success', 'review_html': review_html})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
    
    else:
        form = ReviewForm(instance=user_review)
    
    context = {
        'video': video,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
        'full_stars': full_stars,
        'half_stars': half_stars,
        'empty_stars': empty_stars,
    }
    return render(request, 'videos/video_details.html', context)


def save_progress(request, video_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_position = data.get('current_position', 0)

            if request.user.is_authenticated:
                video = get_object_or_404(Video, pk=video_id)
                progress, created = WatchProgress.objects.get_or_create(
                    user=request.user, video=video
                )
                progress.current_position = int(current_position)
                progress.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



def recent_videos(request):
    videos = Video.objects.order_by('-created_at')[:10]
    context = {
        'videos': videos
    }
    return render(request, 'videos/recent_videos.html', context)



def add_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        release_date = request.POST.get('release_date')
        duration_str = request.POST.get('duration')
        category_id = request.POST.get('category')

        if not all([title, description, video_file, thumbnail, release_date, duration_str, category_id]):
            messages.error(request, 'All fields are required.')
            return render(request, 'videos/add-video.html', {'categories': Category.objects.all()})

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected.')
            return render(request, 'videos/add-video.html', {'categories': Category.objects.all()})

        try:
            hours, minutes, seconds = map(int, duration_str.split(':'))
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            messages.error(request, 'Invalid duration format. Use hh:mm:ss.')
            return render(request, 'videos/add-video.html', {'categories': Category.objects.all()})

        video = Video(
            title=title,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail,
            release_date=release_date,
            duration=duration,
            category=category,
            user = request.user
        )

        try:
            video.save()  
            messages.success(request, 'Video added successfully!')
            return redirect('home')  
        except Exception as e:
            messages.error(request, f'Error adding video: {e}')
            return render(request, 'videos/add-video.html', {'categories': Category.objects.all()})
    else:
        categories = Category.objects.all()
        return render(request, 'videos/add-video.html', {'categories': categories})



def update_video(request, slug):
    video = get_object_or_404(Video, slug=slug)

    if request.user != video.user:
        messages.error(request, 'You are not authorized to edit this video.')
        return redirect('video_details', slug=video.slug)  
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        release_date = request.POST.get('release_date')
        duration_str = request.POST.get('duration')
        category_id = request.POST.get('category')

        # Validating input fields
        if not all([title, description, release_date, duration_str, category_id]):
            messages.error(request, 'All fields except video and thumbnail are required.')
            return render(request, 'videos/update-video.html', {'video': video, 'categories': Category.objects.all()})

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected.')
            return render(request, 'videos/update-video.html', {'video': video, 'categories': Category.objects.all()})

        try:
            # duration split gareko 3 parts ma
            duration_parts = duration_str.split(':')
            if len(duration_parts) != 3:
                raise ValueError("Invalid duration format")
            
            hours, minutes, seconds = map(int, duration_parts)
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            messages.error(request, 'Invalid duration format. Use hh:mm:ss.')
            return render(request, 'videos/update-video.html', {'video': video, 'categories': Category.objects.all()})
        # Update exissting field
        video.title = title
        video.description = description
        video.release_date = release_date
        video.duration = duration
        video.category = category

        # Only update the video file and thumbnail if upload gareko xa vane
        if video_file:
            video.video_file = video_file
        if thumbnail:
            video.thumbnail = thumbnail

        try:
            video.save()  
            messages.success(request, 'Video updated successfully!')
            return redirect('video_details', slug=video.slug)  
        except Exception as e:
            messages.error(request, f'Error updating video: {e}')
            return render(request, 'videos/update-video.html', {'video': video, 'categories': Category.objects.all()})
    else:
        categories = Category.objects.all()
        return render(request, 'videos/update-video.html', {'video': video, 'categories': categories})
    

def delete_video(request, slug):
    video = get_object_or_404(Video, slug=slug)

    if request.user != video.user:
        messages.error(request, 'You are not authorized to delete this video.')
        return redirect('video_details', slug=video.slug)

    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('home')  

    return render(request, 'videos/confirm_delete.html', {'video': video})


def increment_watch_count(request, slug):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=slug)
        video.increment_watch_count()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
