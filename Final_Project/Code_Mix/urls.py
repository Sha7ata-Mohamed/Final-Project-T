from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('type/<str:diff_level>/', views.choose_type, name='choose_type'),
    path('type/<str:diff_level>/', views.choose_type, name='choose_type'),
    path('easy/<int:question_id>/', views.easy_category, name='easy_category'),
    path('question2/<int:question_id>/', views.Question_Two, name='question_two'),
]