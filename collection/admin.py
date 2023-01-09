from django.contrib import admin
from .models import *


# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_filter = ("director", "tags", "release_date",)
    list_display = ("title", "release_date", "director",)
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "movie")


admin.site.register(Tag)
admin.site.register(Director)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)
