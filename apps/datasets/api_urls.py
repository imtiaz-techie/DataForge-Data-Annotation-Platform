from django.urls import path
from . import api_views

app_name = 'api_datasets'

urlpatterns = [
    path('', api_views.all_datasets_stats, name='all_stats'),
    path('<int:pk>/stats/', api_views.dataset_stats, name='stats'),
]
