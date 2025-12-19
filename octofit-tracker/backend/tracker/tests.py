from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Activity, Team, Workout
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class TrackerModelsTest(TestCase):
    def test_create_activity_and_workout_and_team(self):
        alice = User.objects.create_user(username='alice', password='password')
        bob = User.objects.create_user(username='bob', password='password')

        team = Team.objects.create(name='Alpha')
        team.members.add(alice, bob)

        activity = Activity.objects.create(
            user=alice,
            activity_type='run',
            date=timezone.now(),
            duration_minutes=30,
            distance_km=5.0,
            calories=400,
            team=team,
        )
        workout = Workout.objects.create(
            user=bob,
            title='Morning Ride',
            date=timezone.now(),
            duration_minutes=45,
            calories=600,
        )

        self.assertEqual(activity.team, team)
        self.assertIn(alice, team.members.all())
        self.assertEqual(workout.user, bob)

    def test_leaderboard_view(self):
        # Create users and activities to test leaderboard aggregation
        alice = User.objects.create_user(username='alice', password='password')
        bob = User.objects.create_user(username='bob', password='password')

        now = timezone.now()
        Activity.objects.create(user=alice, activity_type='run', date=now, duration_minutes=30, distance_km=5.0, calories=300)
        Activity.objects.create(user=alice, activity_type='cycle', date=now, duration_minutes=60, distance_km=20.0, calories=700)
        Activity.objects.create(user=bob, activity_type='run', date=now, duration_minutes=20, distance_km=4.0, calories=250)

        url = reverse('tracker:leaderboard') if 'tracker' in [u.namespace for u in []] else reverse('leaderboard')
        # Call leaderboard view
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.get('/api/leaderboard/?limit=2')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Alice should be first (25 km total) then Bob
        self.assertGreaterEqual(len(data), 2)
        self.assertEqual(data[0]['user']['username'], 'alice')
        self.assertAlmostEqual(data[0]['total_distance_km'], 25.0, places=1)
        self.assertEqual(data[1]['user']['username'], 'bob')

