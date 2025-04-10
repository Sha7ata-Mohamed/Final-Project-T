from django.urls import path
from . import views
urlpatterns = [
    path('questions/', views.show_questions , name='show_questions'),
    path('questions/options/<int:question_id>', views.show_options, name='show_options'),
]