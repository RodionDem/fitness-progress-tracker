from django.shortcuts import render, redirect
from .models import WorkoutPlan, Exercise, ProgressRecord, WorkoutSession
from .forms import WorkoutPlanForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def create_workout_plan(request):
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            return redirect('workout_plan_list')
    else:
        form = WorkoutPlanForm()
    return render(request, 'workout_plans/create_workout_plan.html', {'form': form})

@login_required
def workout_plan_list(request):
    plans = WorkoutPlan.objects.filter(created_by=request.user)
    return render(request, 'workout_plans/workout_plan_list.html', {'plans': plans})


@login_required
def dashboard(request):
    workout_plans_count = WorkoutPlan.objects.filter(created_by=request.user).count()
    exercises_count = Exercise.objects.filter(workout_plan__created_by=request.user).count()
    sessions_count = WorkoutSession.objects.filter(user=request.user).count()
    progress_count = ProgressRecord.objects.filter(user=request.user).count()

    context = {
        'workout_plans_count': workout_plans_count,
        'exercises_count': exercises_count,
        'sessions_count': sessions_count,
        'progress_count': progress_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def exercise_list(request, plan_id):
    plan = get_object_or_404(
        WorkoutPlan,
        id=plan_id,
        created_by=request.user
    )

    exercises = plan.exercises.all()

    return render(
        request,
        "exercises/exercise_list.html",
        {
            "plan": plan,
            "exercises": exercises
        }
    )
