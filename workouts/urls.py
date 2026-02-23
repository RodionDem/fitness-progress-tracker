from django.urls import path
from . import views
from .views import (
    WorkoutSessionCreateView,
    WorkoutSessionUpdateView,
    WorkoutSessionDeleteView,
    WorkoutPlanUpdateView,
    WorkoutPlanDeleteView,
)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plans/', views.workout_plan_list, name='workout_plan_list'),
    path('plans/create/', views.create_workout_plan, name='create_workout_plan'),
    path('plans/<int:pk>/edit/', WorkoutPlanUpdateView.as_view(), name='workout_plan_update'),
    path('plans/<int:pk>/delete/', WorkoutPlanDeleteView.as_view(), name='workout_plan_delete'),
    path('plans/<int:plan_id>/exercises/', views.exercise_list, name='exercise_list'),
    path('sessions/', views.workout_session_list, name='workout_session_list'),
    path('sessions/create/', WorkoutSessionCreateView.as_view(), name='session-create'),
    path('sessions/<int:pk>/edit/', WorkoutSessionUpdateView.as_view(), name='session-update'),
    path('sessions/<int:pk>/delete/', WorkoutSessionDeleteView.as_view(), name='session-delete'),
    path('sessions/<int:pk>/toggle/', views.toggle_session_completed, name='toggle_session_completed'),
    path('sessions/<int:pk>/', views.workout_session_detail, name='workout_session_detail'),
]
