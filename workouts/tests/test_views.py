from django.test import TestCase
from django.urls import reverse
from workouts.models import User, WorkoutPlan, Exercise, WorkoutSession, ProgressRecord


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.plan = WorkoutPlan.objects.create(
            name="Test Plan",
            description="Plan description",
            created_by=self.user
        )

        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            description="Exercise description",
            workout_plan=self.plan,
            duration_minutes=30,
            repetitions=10
        )

        self.session = WorkoutSession.objects.create(
            user=self.user,
            workout_plan=self.plan,
            completed=False
        )

        self.progress = ProgressRecord.objects.create(
            user=self.user,
            exercise=self.exercise,
            workout_session=self.session,
            weight_used=20,
            repetitions=10,
            duration_minutes=30,
            notes="Good"
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workout Plans")
        self.assertContains(response, "Exercises")
        self.assertContains(response, "Sessions")
        self.assertContains(response, "Progress Records")
        self.assertContains(response, "1")

    def test_workout_plan_list_view(self):
        response = self.client.get(reverse("workout_plan_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.plan.name)

    def test_exercise_list_view(self):
        url = reverse("exercise_list", kwargs={"plan_id": self.plan.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.exercise.name)

    def test_workout_session_list_view(self):
        response = self.client.get(reverse("workout_session_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.session.workout_plan.name)

    def test_progress_record_list_view(self):
        response = self.client.get(reverse("progress_record_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.progress.exercise.name)
