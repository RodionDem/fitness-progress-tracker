from django import forms
from .models import WorkoutPlan, WorkoutSession, Exercise


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['workout_plan', 'completed']
        widgets = {
            'completed': forms.CheckboxInput(),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'duration_minutes', 'repetitions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
