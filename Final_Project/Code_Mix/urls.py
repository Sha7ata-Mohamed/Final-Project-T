from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('type/<str:diff_level>/', views.choose_type, name='choose_type'),
    path('type/<str:diff_level>/', views.choose_type, name='choose_type'),
    path('question1/<int:question_id>/', views.Question_One, name='question_one'),
    path('question2/<int:question_id>/', views.Question_Two, name='question_two'),
]