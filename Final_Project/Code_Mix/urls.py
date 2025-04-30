from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.home), name='home'),
    path('type/<str:diff_level>/', login_required(views.choose_type), name='choose_type'),
    path('choose_category/', login_required(views.choose_category), name='choose_category'),
    path('easy/<int:id>/', login_required(views.easy_category), name='easy_category'),
    path('medium/<int:id>/', login_required(views.medium_category), name='medium_category'),
    path('hard/<int:id>/', login_required(views.hard_category), name='hard_category'),
    path('submit_answer/', login_required(views.submit_answer), name='submit_answer'),
    path('scores/', login_required(views.show_scores), name='scores'),
    path('signup/', views.signup, name='signup'),
    path('profile/', login_required(views.profile), name='profile'),
]
