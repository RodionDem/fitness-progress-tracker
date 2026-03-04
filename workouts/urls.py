from django.urls import path
from . import views
from .views import (
    WorkoutSessionCreateView,
    WorkoutSessionUpdateView,
    WorkoutSessionDeleteView,
    WorkoutPlanUpdateView,
    WorkoutPlanDeleteView,
    ExerciseCreateView,
    ExerciseUpdateView,
    ExerciseDeleteView,
    ProgressRecordCreateView, ProgressRecordListView,
)

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Workout Plans
    path('plans/', views.workout_plan_list, name='workout_plan_list'),
    path('plans/create/', views.create_workout_plan, name='create_workout_plan'),
    path('plans/<int:pk>/edit/', WorkoutPlanUpdateView.as_view(), name='workout_plan_update'),
    path('plans/<int:pk>/delete/', WorkoutPlanDeleteView.as_view(), name='workout_plan_delete'),

    # Exercises for a specific plan
    path('plans/<int:plan_id>/exercises/', views.exercise_list, name='exercise_list'),
    path('plans/<int:plan_id>/exercises/create/', ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercises/<int:pk>/edit/', ExerciseUpdateView.as_view(), name='exercise_update'),
    path('exercises/<int:pk>/delete/', ExerciseDeleteView.as_view(), name='exercise_delete'),

    # Workout Sessions
    path('sessions/', views.workout_session_list, name='workout_session_list'),
    path('sessions/create/', WorkoutSessionCreateView.as_view(), name='workout_session_create'),
    path('sessions/<int:pk>/edit/', WorkoutSessionUpdateView.as_view(), name='workout_session_update'),
    path('sessions/<int:pk>/delete/', WorkoutSessionDeleteView.as_view(), name='workout_session_delete'),
    path('sessions/<int:pk>/toggle/', views.toggle_session_completed, name='toggle_session_completed'),
    path('sessions/<int:pk>/', views.workout_session_detail, name='workout_session_detail'),

    # Progress Records
    path('progress/', ProgressRecordListView.as_view(), name='progress_record_list'),
    path('sessions/<int:session_id>/progress/add/', ProgressRecordCreateView.as_view(),name='progress_record_create'),
    path('progress/<int:pk>/edit/', views.ProgressRecordUpdateView.as_view(), name='progress_record_update'),
    path('progress/<int:pk>/delete/', views.ProgressRecordDeleteView.as_view(), name='progress_record_delete'),
]
