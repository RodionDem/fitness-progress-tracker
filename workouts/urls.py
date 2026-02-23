from django.urls import path
from . import views
from .views import WorkoutSessionCreateView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plans/', views.workout_plan_list, name='workout_plan_list'),
    path('plans/create/', views.create_workout_plan, name='create_workout_plan'),
    path('plans/<int:plan_id>/exercises/', views.exercise_list, name='exercise_list'),

    path('sessions/', views.workout_session_list, name='workout_session_list'),
    path('sessions/create/', views.create_workout_session, name='create_workout_session'),
    path('sessions/<int:session_id>/toggle/', views.toggle_session_completed, name='toggle_session_completed'),
    path("sessions/<int:session_id>/", views.workout_session_detail, name="workout_session_detail"),
    path("sessions/create/", WorkoutSessionCreateView.as_view(),name="session-create"),
]
