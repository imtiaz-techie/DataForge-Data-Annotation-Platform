from django.urls import path
from . import api_views

app_name = 'api_dashboard'

urlpatterns = [
    path('stats/', api_views.dashboard_stats, name='stats'),
]
