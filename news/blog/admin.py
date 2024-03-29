from django.contrib import admin

from blog.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', )
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)