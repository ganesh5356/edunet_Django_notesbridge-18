from django.contrib import admin
from .models import Resource, Bookmark, Doubt, Download

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'semester', 'uploaded_by', 'created_at')
    list_filter = ('department', 'semester', 'resource_type')
    search_fields = ('title', 'subject')

@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('subject', 'asked_by', 'resolved', 'created_at')
    list_filter = ('resolved', 'subject')
    search_fields = ('question', 'asked_by')

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('resource_id', 'user', 'timestamp')
    list_filter = ('timestamp',)

admin.site.register(Bookmark)