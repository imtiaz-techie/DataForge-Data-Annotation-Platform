from django.urls import path
from . import views

app_name = 'export'

urlpatterns = [
    path('<int:dataset_pk>/<str:fmt>/', views.export_dataset, name='export'),
]
