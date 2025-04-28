from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('type/<str:diff_level>/', views.choose_type, name='choose_type'),
    path('choose_category/', views.choose_category, name='choose_category'),
    path('easy/<int:id>/', views.easy_category, name='easy_category'),
    path('medium/<int:id>/', views.medium_category, name='medium_category'),
    path('hard/<int:id>/', views.hard_category, name='hard_category'),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('scores/', views.show_scores, name='show_scores'),
]