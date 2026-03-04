from django.test import TestCase
from workouts.models import WorkoutPlan, WorkoutSession, Exercise, ProgressRecord, User


class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.plan = WorkoutPlan.objects.create(name="Test Plan", description="Test description", created_by=self.user)
        self.exercise = Exercise.objects.create(
            name="Push Up", workout_plan=self.plan, duration_minutes=10, repetitions=15
        )

        self.session = WorkoutSession.objects.create(user=self.user, workout_plan=self.plan)
        self.progress = ProgressRecord.objects.create(
            user=self.user,
            exercise=self.exercise,
            workout_session=self.session,
            weight_used=20,
            repetitions=15,
            duration_minutes=10,
        )

    def test_workout_plan_creation(self):
        self.assertEqual(self.plan.name, "Test Plan")
        self.assertEqual(self.plan.created_by, self.user)

    def test_exercise_creation(self):
        self.assertEqual(self.exercise.workout_plan, self.plan)
        self.assertEqual(self.exercise.repetitions, 15)

    def test_workout_session_creation(self):
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.workout_plan, self.plan)

    def test_progress_record_creation(self):
        self.assertEqual(self.progress.user, self.user)
        self.assertEqual(self.progress.exercise, self.exercise)
        self.assertEqual(self.progress.repetitions, 15)
