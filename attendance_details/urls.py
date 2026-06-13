from django.urls import path
from . import views

urlpatterns = [
    path('attendance/record/<int:id>/edit/', views.attendance_record_edit, name='attendance_record_edit'),
    path('attendance/record/<int:id>/delete/', views.attendance_record_delete, name='attendance_record_delete'),
]