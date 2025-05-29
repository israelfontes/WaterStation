from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('users/', include('apps.users.urls')),
    path('monitoring/', include('apps.monitoring.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/monitoring/', include('apps.monitoring.api_urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# apps/users