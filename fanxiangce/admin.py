from django.contrib import admin
from .models import Photo, Album, Profile

# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,               {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    # ]
    list_display = ('url', 'about', 'timestamp')
    # list_filter = ['timestamp']
    search_fields = ['url']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
