from django.db import models
from django.urls import reverse
from users.models import CustomUser
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class MovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category__name__iexact='Movie')


class TVShowManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category__name__iexact='TV Show')



class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/' , max_length=1000)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    release_date = models.DateField()
    duration = models.DurationField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)
    watch_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    
    class Meta:
        abstract = False

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"slug": self.slug})
    
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def user_review(self, user):
        return self.reviews.filter(user=user).first()

    def increment_watch_count(self):
        self.watch_count += 1
        self.save()



class WatchProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    current_position = models.PositiveIntegerField(default=0)  
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} watched {self.video.title}"


class Review(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.video.title} - {self.rating}'



class Movie(Video):
    objects = MovieManager()

    class Meta:
        proxy = True
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def get_type(self):
        return "Movie"



class TVShow(Video):
    objects = TVShowManager()

    class Meta:
        proxy = True
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'

    def get_type(self):
        return "TV Show"




