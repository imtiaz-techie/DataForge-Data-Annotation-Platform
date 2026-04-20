from django.urls import path
from . import views

app_name = 'annotations'

urlpatterns = [
    path('label/<int:item_pk>/', views.label_item, name='label_item'),
    path('submit/<int:item_pk>/', views.submit_label, name='submit_label'),
    path('queue/<int:dataset_pk>/', views.annotation_queue, name='queue'),
    path('review/<int:dataset_pk>/', views.review_annotations, name='review'),
    path('verify/<int:annotation_pk>/', views.verify_annotation, name='verify'),
    path('release/<int:item_pk>/', views.release_lock, name='release_lock'),
]
