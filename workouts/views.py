from django.shortcuts import render, redirect, get_object_or_404
from .models import WorkoutPlan, Exercise, ProgressRecord, WorkoutSession
from .forms import WorkoutPlanForm, WorkoutSessionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required
def workout_session_list(request):
    sessions = WorkoutSession.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workout_sessions/workout_session_list.html', {'sessions': sessions})

@login_required
def create_workout_session(request):
    if request.method == "POST":
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            messages.success(request, "Workout session created successfully!")
            return redirect('workout_session_list')
    else:
        form = WorkoutSessionForm()
    return render(request, 'workout_sessions/create_workout_session.html', {'form': form})

@login_required
def toggle_session_completed(request, session_id):
    session = get_object_or_404(WorkoutSession, id=session_id, user=request.user)
    session.completed = not session.completed
    session.save()
    messages.success(request, f"Session marked as {'completed' if session.completed else 'not completed'}.")
    return redirect('workout_session_list')
