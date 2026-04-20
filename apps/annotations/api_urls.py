from django.urls import path
from . import api_views

app_name = 'api_annotations'

urlpatterns = [
    path('next/<int:dataset_pk>/', api_views.get_next_task, name='next_task'),
    path('submit/<int:item_pk>/', api_views.api_submit_label, name='submit'),
    path('mine/', api_views.my_annotations, name='my_annotations'),
]
