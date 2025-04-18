# quizapp/urls.py

from django.contrib import admin  # Add this import
from django.urls import path
from . import views  # Import your views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('topics/', views.topics, name='topics'),  # Topics page
    path('quiz/', views.quiz, name='quiz'),  # Quiz page
    path('topics/quiz.html/', views.quiz, name='quiz'),
     path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
