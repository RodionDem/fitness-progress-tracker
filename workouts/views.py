from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator

from .models import WorkoutPlan, Exercise, ProgressRecord, WorkoutSession
from .forms import WorkoutPlanForm, WorkoutSessionForm, ExerciseForm, ProgressRecordForm


def get_first_plan(user):
    """Return the first workout plan for the user."""
    return WorkoutPlan.objects.filter(created_by=user).first()


@login_required
def dashboard(request):
    first_plan = get_first_plan(request.user)
    first_session = WorkoutSession.objects.filter(user=request.user).first()

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
        "first_plan": first_plan,
        "first_session": first_session,
        "progress_page_exists": ProgressRecord.objects.filter(
            user=request.user
        ).exists(),
    }
    return render(request, "dashboard/dashboard.html", context)



@login_required
def workout_plan_list(request):
    first_plan = get_first_plan(request.user)
    search_query = request.GET.get("search", "")
    plans = WorkoutPlan.objects.filter(created_by=request.user)
    if search_query:
        plans = plans.filter(name__icontains=search_query)
    plans = plans.order_by("-id")

    paginator = Paginator(plans, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "first_plan": first_plan,
    }
    return render(request, "workout_plans/workout_plan_list.html", context)


@login_required
def create_workout_plan(request):
    first_plan = get_first_plan(request.user)
    if request.method == "POST":
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.created_by = request.user
            plan.save()
            messages.success(request, "Workout plan created successfully!")
            return redirect("workout_plan_list")
    else:
        form = WorkoutPlanForm()

    context = {"form": form, "first_plan": first_plan}
    return render(request, "workout_plans/create_workout_plan.html", context)


@login_required
def exercise_list(request, plan_id):
    plan = get_object_or_404(
        WorkoutPlan,
        id=plan_id,
        created_by=request.user,
    )
    search_query = request.GET.get("search", "")
    exercises = plan.exercises.all()
    if search_query:
        exercises = exercises.filter(name__icontains=search_query)
    exercises = exercises.order_by("id")

    paginator = Paginator(exercises, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    first_plan = get_first_plan(request.user)

    context = {
        "plan": plan,
        "page_obj": page_obj,
        "search_query": search_query,
        "first_plan": first_plan,
    }
    return render(request, "exercises/exercise_list.html", context)


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "exercises/exercise_form.html"

    def form_valid(self, form):
        plan_id = self.kwargs.get("plan_id")
        plan = get_object_or_404(
            WorkoutPlan, id=plan_id, created_by=self.request.user
        )
        form.instance.workout_plan = plan
        messages.success(self.request, "Exercise created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "exercise_list",
            kwargs={"plan_id": self.kwargs.get("plan_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_id = self.kwargs.get("plan_id")
        context["plan"] = get_object_or_404(
            WorkoutPlan, id=plan_id, created_by=self.request.user
        )
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "exercises/exercise_form.html"

    def get_queryset(self):
        return Exercise.objects.filter(workout_plan__created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Exercise updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "exercise_list", kwargs={"plan_id": self.object.workout_plan.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercise
    template_name = "exercises/exercise_confirm_delete.html"

    def get_queryset(self):
        return Exercise.objects.filter(workout_plan__created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Exercise deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "exercise_list", kwargs={"plan_id": self.object.workout_plan.id}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


@login_required
def workout_session_list(request):
    first_plan = get_first_plan(request.user)
    search_query = request.GET.get("search", "")
    sessions = WorkoutSession.objects.filter(user=request.user)
    if search_query:
        sessions = sessions.filter(workout_plan__name__icontains=search_query)
    sessions = sessions.order_by("-date")
    paginator = Paginator(sessions, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "first_plan": first_plan,
    }
    return render(request, "workout_sessions/workout_session_list.html", context)


@login_required
def workout_session_detail(request, pk):
    first_plan = get_first_plan(request.user)
    session = get_object_or_404(WorkoutSession, id=pk, user=request.user)
    exercises = session.workout_plan.exercises.all()
    progress_records = session.progress_records.select_related("exercise")
    context = {
        "session": session,
        "exercises": exercises,
        "progress_records": progress_records,
        "first_plan": first_plan,
    }
    return render(
        request, "workout_sessions/workout_session_detail.html", context
    )


@login_required
def toggle_session_completed(request, pk):
    session = get_object_or_404(WorkoutSession, id=pk, user=request.user)
    session.completed = not session.completed
    session.save()
    messages.success(
        request,
        f"Session marked as {'completed' if session.completed else 'not completed'}.",
    )
    return redirect("workout_session_list")


class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = "workout_sessions/workout_session_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Workout session created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workout_session_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class WorkoutSessionUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = "workout_sessions/workout_session_form.html"

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Workout session updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workout_session_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    template_name = "workout_sessions/workout_session_confirm_delete.html"
    success_url = reverse_lazy("workout_session_list")

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Workout session deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class WorkoutPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "workout_plans/workout_plan_form.html"
    success_url = reverse_lazy("workout_plan_list")

    def get_queryset(self):
        return WorkoutPlan.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Workout plan updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class WorkoutPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutPlan
    template_name = "workout_plans/workout_plan_confirm_delete.html"
    success_url = reverse_lazy("workout_plan_list")

    def get_queryset(self):
        return WorkoutPlan.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Workout plan deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ProgressRecordListView(LoginRequiredMixin, ListView):
    model = ProgressRecord
    template_name = "progress/progress_record_list.html"
    context_object_name = "page_obj"

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        qs = ProgressRecord.objects.filter(user=self.request.user).order_by('-id')
        if search_query:
            qs = qs.filter(exercise__name__icontains=search_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), 2)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["search_query"] = self.request.GET.get("search", "")
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ProgressRecordCreateView(LoginRequiredMixin, CreateView):
    model = ProgressRecord
    form_class = ProgressRecordForm
    template_name = "progress/progress_record_form.html"

    def get_session(self):
        return get_object_or_404(
            WorkoutSession,
            id=self.kwargs.get("session_id"),
            user=self.request.user,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["session"] = self.get_session()
        return kwargs

    def form_valid(self, form):
        session = self.get_session()
        form.instance.user = self.request.user
        form.instance.workout_session = session
        messages.success(self.request, "Progress record added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "workout_session_detail",
            kwargs={"pk": self.kwargs.get("session_id")},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session"] = self.get_session()
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ProgressRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = ProgressRecord
    form_class = ProgressRecordForm
    template_name = "progress/progress_record_form.html"

    def get_queryset(self):
        return ProgressRecord.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["session"] = self.object.workout_session
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Progress record updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "workout_session_detail",
            kwargs={"pk": self.object.workout_session.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session"] = self.object.workout_session
        context["first_plan"] = get_first_plan(self.request.user)
        return context


class ProgressRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = ProgressRecord
    template_name = "progress/progress_record_confirm_delete.html"

    def get_queryset(self):
        return ProgressRecord.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Progress record deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "workout_session_detail",
            kwargs={"pk": self.object.workout_session.id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session"] = self.object.workout_session
        context["first_plan"] = get_first_plan(self.request.user)
        return context


