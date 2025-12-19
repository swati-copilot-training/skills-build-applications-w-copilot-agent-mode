from django.contrib import admin
from .models import Profile, Activity, Team, Workout


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'date', 'duration_minutes')
    list_filter = ('activity_type', 'date')
    search_fields = ('user__username',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count', 'created_at')
    search_fields = ('name',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'duration_minutes')
    list_filter = ('date',)
    search_fields = ('user__username', 'title')
