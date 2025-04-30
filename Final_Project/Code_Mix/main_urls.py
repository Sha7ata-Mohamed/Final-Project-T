from django.urls import path, include

urlpatterns = [
    path('', include('Code_Mix.urls')),
    
    path('progress/', include('Code_Mix.urls_progress')),
    
    path('auth/', include('Code_Mix.urls_auth')),
]
