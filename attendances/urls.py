from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:id>/', views.attendance_detail, name='attendance_detail'),
    path('attendance/<int:id>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:id>/delete/', views.attendance_delete, name='attendance_delete'),
    path('attendance/<int:pk>/mark/', views.attendance_mark, name='attendance_mark'),
]