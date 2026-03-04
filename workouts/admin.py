from django.contrib import admin
from .models import WorkoutPlan, Exercise, WorkoutSession, ProgressRecord


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 0
    fields = ("name",)
    readonly_fields = ()
    show_change_link = True


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name", "created_by__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "workout_plan")
    search_fields = ("name", "workout_plan__name")
    list_filter = ("workout_plan",)
    ordering = ("workout_plan", "name")


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "workout_plan", "date", "completed")
    list_filter = ("completed", "date", "workout_plan")
    search_fields = ("user__username", "workout_plan__name")
    ordering = ("-date",)
    date_hierarchy = "date"


@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "workout_session", "exercise")
    search_fields = (
        "user__username",
        "exercise__name",
        "workout_session__workout_plan__name",
    )
    list_filter = ("exercise", "workout_session")
    ordering = ("-id",)
