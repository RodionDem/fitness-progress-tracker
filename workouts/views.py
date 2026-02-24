from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from .models import WorkoutPlan, Exercise, ProgressRecord, WorkoutSession
from .forms import WorkoutPlanForm, WorkoutSessionForm


@login_required
def dashboard(request):
    context = {
        "workout_plans_count": WorkoutPlan.objects.filter(
            created_by=request.user
        ).count(),
        "exercises_count": Exercise.objects.filter(
            workout_plan__created_by=request.user
        ).count(),
        "sessions_count": WorkoutSession.objects.filter(
            user=request.user
        ).count(),
        "progress_count": ProgressRecord.objects.filter(
            user=request.user
        ).count(),
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def workout_plan_list(request):
    query = request.GET.get("q")
    plans = WorkoutPlan.objects.filter(created_by=request.user)
    if query:
        plans = plans.filter(name__icontains=query)
    plans = plans.order_by("-id")
    paginator = Paginator(plans, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
    }
    return render(
        request,
        "workout_plans/workout_plan_list.html",
        context,
    )


@login_required
def create_workout_plan(request):
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            messages.success(
                request,
                "Workout plan created successfully!"
            )
            return redirect("workout_plan_list")
    else:
        form = WorkoutPlanForm()

    return render(
        request,
        "workout_plans/create_workout_plan.html",
        {"form": form},
    )


@login_required
def exercise_list(request, plan_id):
    plan = get_object_or_404(
        WorkoutPlan,
        id=plan_id,
        created_by=request.user,
    )
    exercises = plan.exercises.all()

    return render(
        request,
        "exercises/exercise_list.html",
        {"plan": plan, "exercises": exercises},
    )


@login_required
def workout_session_list(request):
    query = request.GET.get("q")
    sessions = WorkoutSession.objects.filter(user=request.user)

    if query:
        sessions = sessions.filter(
            workout_plan__name__icontains=query
        )

    sessions = sessions.order_by("-date")
    paginator = Paginator(sessions, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
    }
    return render(
        request,
        "workout_sessions/workout_session_list.html",
        context,
    )


@login_required
def workout_session_detail(request, pk):
    session = get_object_or_404(
        WorkoutSession,
        id=pk,
        user=request.user,
    )
    exercises = session.workout_plan.exercises.all()
    progress_records = session.progress_records.select_related("exercise")

    context = {
        "session": session,
        "exercises": exercises,
        "progress_records": progress_records,
    }
    return render(
        request,
        "workout_sessions/workout_session_detail.html",
        context,
    )


@login_required
def toggle_session_completed(request, pk):
    session = get_object_or_404(
        WorkoutSession,
        id=pk,
        user=request.user,
    )
    session.completed = not session.completed
    session.save()

    messages.success(
        request,
        f"Session marked as "
        f"{'completed' if session.completed else 'not completed'}."
    )
    return redirect("workout_session_list")


class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = "workout_sessions/workout_session_form.html"
    success_url = reverse_lazy("workout_session_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request,
            "Workout session created successfully!",
        )
        return super().form_valid(form)


class WorkoutSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = "workout_sessions/workout_session_form.html"
    success_url = reverse_lazy("workout_session_list")

    def get_queryset(self):
        return WorkoutSession.objects.filter(
            user=self.request.user
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Workout session updated successfully!",
        )
        return super().form_valid(form)


class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    template_name = (
        "workout_sessions/workout_session_confirm_delete.html"
    )
    success_url = reverse_lazy("workout_session_list")

    def get_queryset(self):
        return WorkoutSession.objects.filter(
            user=self.request.user
        )

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Workout session deleted successfully!",
        )
        return super().delete(request, *args, **kwargs)


class WorkoutPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "workout_plans/workout_plan_form.html"
    success_url = reverse_lazy("workout_plan_list")

    def get_queryset(self):
        return WorkoutPlan.objects.filter(
            created_by=self.request.user
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Workout plan updated successfully!",
        )
        return super().form_valid(form)


class WorkoutPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutPlan
    template_name = (
        "workout_plans/workout_plan_confirm_delete.html"
    )
    success_url = reverse_lazy("workout_plan_list")

    def get_queryset(self):
        return WorkoutPlan.objects.filter(
            created_by=self.request.user
        )

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Workout plan deleted successfully!",
        )
        return super().delete(request, *args, **kwargs)
