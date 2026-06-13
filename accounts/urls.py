from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-teacher/', views.create_teacher_user, name='create_teacher'),
    path('create-student/', views.create_student_user, name='create_student'),
]
