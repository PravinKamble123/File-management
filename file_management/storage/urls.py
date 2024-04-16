
from django.urls import path

from . import views

app_name = 'storage'

urlpatterns = [

    path('files/upload/', views.upload_file),   
    path('files/<int:pk>/', views.file_detail),
    path('files/<int:pk>/edit/', views.update_file),
    path('files/<int:pk>/move/', views.move_file),
    path('files/', views.my_files),
    path('files/<int:pk>/delete/', views.delete_file),

    path('folders/create/', views.create_folder),   
    path('folders/<int:pk>/', views.folder_detail, name='get-detail'),
    path('folders/<int:pk>/edit/', views.edit_folder, name='edit-folder'),
    path('folders/<int:pk>/move/', views.move_folder),
    path('folders/', views.my_folders),
    path('folders/<int:pk>/delete/', views.delete_folder)
]