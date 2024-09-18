from django.contrib import admin
from .models import Category, Video, Movie, TVShow, WatchProgress, Review
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release_date', 'duration')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release_date', 'duration')

@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release_date', 'duration')

admin.site.register(WatchProgress)
admin.site.register(Review)