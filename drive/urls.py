from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('create_folder/', views.create_folder, name='create_folder'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('delete/<str:item_type>/<int:item_id>/', views.delete, name='delete'),
]
