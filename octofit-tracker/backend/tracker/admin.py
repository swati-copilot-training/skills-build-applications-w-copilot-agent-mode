from django.contrib import admin
from .models import Profile, Activity


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'date', 'duration_minutes')
    list_filter = ('activity_type', 'date')
    search_fields = ('user__username',)
