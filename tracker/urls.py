from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('skills/', views.skills_list_view, name='skills_list'),
    path('skills/add/', views.skill_create_view, name='skill_add'),
    path('skills/<int:pk>/edit/', views.skill_edit_view, name='skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete_view, name='skill_delete'),
    path('goals/', views.goals_view, name='goals'),
    path('goals/<int:pk>/toggle/', views.toggle_goal_view, name='toggle_goal'),
    path('goals/<int:pk>/delete/', views.delete_goal_view, name='delete_goal'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]