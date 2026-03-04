from typing import Optional

from django import forms
from .models import (
    WorkoutPlan,
    WorkoutSession,
    Exercise,
    ProgressRecord,
)


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ["workout_plan", "completed"]
        widgets = {
            "completed": forms.CheckboxInput(),
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            "name",
            "description",
            "duration_minutes",
            "repetitions",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class ProgressRecordForm(forms.ModelForm):
    class Meta:
        model = ProgressRecord
        fields = [
            "exercise",
            "weight_used",
            "repetitions",
            "duration_minutes",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(
        self,
        *args,
        session: Optional[WorkoutSession] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if session is not None:
            self.fields["exercise"].queryset = (
                session.workout_plan.exercises.all()
            )