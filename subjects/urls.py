from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:id>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:id>/delete/', views.subject_delete, name='subject_delete'),
]