from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plans/', views.workout_plan_list, name='workout_plan_list'),
    path('plans/create/', views.create_workout_plan, name='create_workout_plan'),
    path('plans/<int:plan_id>/exercises/', views.exercise_list, name='exercise_list'),
]
