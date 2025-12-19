from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username


class Team(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('run', 'Running'),
        ('walk', 'Walking'),
        ('cycle', 'Cycling'),
        ('swim', 'Swimming'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='activities')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} {self.activity_type} {self.date.date()}"


class Workout(models.Model):
    """A user workout session which may summarize several activities or be a planned workout."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    calories = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username} - {self.date.date()})"