from django.test import TestCase
from workouts.forms import WorkoutPlanForm, ExerciseForm, WorkoutSessionForm, ProgressRecordForm
from workouts.models import WorkoutPlan, Exercise, WorkoutSession, ProgressRecord, User


class FormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.plan = WorkoutPlan.objects.create(name="Test Plan", description="Desc", created_by=self.user)
        self.exercise = Exercise.objects.create(name="Push Up", workout_plan=self.plan)

    def test_workout_plan_form_valid(self):
        form = WorkoutPlanForm(data={"name": "New Plan", "description": "Some desc"})
        self.assertTrue(form.is_valid())

    def test_exercise_form_valid(self):
        form = ExerciseForm(data={"name": "Pull Up", "workout_plan": self.plan.id, "duration_minutes": 5, "repetitions": 10})
        self.assertTrue(form.is_valid())

    def test_workout_session_form_valid(self):
        form = WorkoutSessionForm(data={"workout_plan": self.plan.id, "completed": True})
        self.assertTrue(form.is_valid())

    def test_progress_record_form_valid(self):
        session = WorkoutSession.objects.create(user=self.user, workout_plan=self.plan)
        form = ProgressRecordForm(
            data={
                "exercise": self.exercise.id,
                "weight_used": 30,
                "repetitions": 12,
                "duration_minutes": 8,
                "notes": "Good session",
            },
            session=session
        )
        self.assertTrue(form.is_valid())
