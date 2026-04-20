from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('dashboard:home'), name='root'),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('datasets/', include('apps.datasets.urls', namespace='datasets')),
    path('annotations/', include('apps.annotations.urls', namespace='annotations')),
    path('export/', include('apps.export.urls', namespace='export')),
    # REST API
    path('api/annotations/', include('apps.annotations.api_urls', namespace='api_annotations')),
    path('api/datasets/', include('apps.datasets.api_urls', namespace='api_datasets')),
    path('api/dashboard/', include('apps.dashboard.api_urls', namespace='api_dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
