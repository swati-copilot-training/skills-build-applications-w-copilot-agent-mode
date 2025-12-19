from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Activity
from django.utils import timezone


User = get_user_model()


class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create_user(username='alice', password='password')
        activity = Activity.objects.create(
            user=user,
            activity_type='run',
            date=timezone.now(),
            duration_minutes=30,
        )
        self.assertEqual(activity.user, user)
        self.assertEqual(activity.activity_type, 'run')
