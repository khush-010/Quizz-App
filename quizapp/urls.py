"""
URL configuration for quizapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from quizgame import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start, name='start'),
    path('accounts/',include("allauth.urls")),
    path('social/signup/', views.signup_redirect, name='signup_redirect'),
    path('home/', views.home, name='home'),
    path("play-quiz/",views.play_quiz, name='playquiz'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('add-questions/', views.add_questions, name='add-questions'),
    path('questions-list/',views.questions_list,name='questions-list'),
    path('modify-question/',views.modify_questions,name='modify-question'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('publish',views.publish,name='publish'),
    path('launchquiz/', views.launch_quiz, name='launchquiz'),
    path('rankings/',views.rankings,name='rankings'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('submitquiz/', views.submit_quiz, name='submitquiz'),
    path('forget-pass/',views.forget_pass,name='forget-pass'),
    path('change-pass/',views.change_pass,name='change-pass'),
    path('confirm-otp/',views.confirm_otp,name="confirm-otp"),
    path('new-pass/',views.new_pass,name="new-pass"),
    path('signout/', views.logout_view, name='signout'),
]