from django.urls import path
from . import views_progress

urlpatterns = [
    path('save_progress/', views_progress.save_progress, name='save_progress'),
    path('resume_progress/', views_progress.resume_progress, name='resume_progress'),
    path('load_progress/<int:progress_id>/', views_progress.load_progress, name='load_progress'),
]
