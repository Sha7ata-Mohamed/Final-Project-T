from django.urls import path
from . import views
urlpatterns = [
    path('question/<int:question_id>/', views.Question_One, name='question_one'),
    path('question2/<int:question_id>/', views.Question_Two, name='question_two'),
]