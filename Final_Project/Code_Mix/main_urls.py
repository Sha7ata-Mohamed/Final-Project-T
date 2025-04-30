from django.urls import path, include

urlpatterns = [
    path('', include('Code_Mix.urls')),
    
    path('progress/', include('Code_Mix.urls_progress')),
    
    path('accounts/', include('Code_Mix.urls_auth')),
]
