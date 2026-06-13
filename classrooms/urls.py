from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<int:id>/', views.class_detail, name='class_detail'),
    path('classes/<int:id>/edit/', views.class_edit, name='class_edit'),
    path('classes/<int:id>/delete/', views.class_delete, name='class_delete'),
]