from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('home/', include('Code_Mix.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

